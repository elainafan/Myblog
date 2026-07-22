---
title: 从零开始的 CUDA Tensor
date: 2025-10-09
categories:
    - AI
slug: ai-programming-lab-02
hidden: true
seriesOrder: 22
---

# 从零开始的 CUDA Tensor

> [!CAUTION]
>
> **本笔记仅供参考，请勿抄袭。**

## 任务

Lab 2 从 PyTorch 的现成接口退回到框架底层。第一部分实现一个只保存 `float` 的 Tensor，负责记录形状、分配内存，并在 CPU 与 GPU 之间迁移数据；第二部分在两种设备上实现 ReLU、Sigmoid 的前向与反向传播。

这时的 Tensor 还不需要切片、转置、reshape 或自动微分。工作集中在存储所有权、复制语义和设备迁移，`.cpu()`、`.gpu()` 返回的对象也必须能够安全地独立存在。

## 环境与文件

复验环境为 Windows 11、CUDA Toolkit 12.4、MSVC 19.44 和 RTX 4060 Laptop GPU。项目只有三个源文件。

```text
Lab2/
├── main.cu
├── tensor.cu
└── tensor.h
```

- `tensor.h` 保存设备枚举、存储对象、Tensor 声明和 CUDA kernel 接口。
- `tensor.cu` 实现内存迁移、打印和激活函数。
- `main.cu` 构造固定测试数据，并比较 CPU、GPU 两条路径。

## 存储所有权

底层存储交给 `Device` 管理。CPU 内存由 `new[]` 分配，GPU 内存由 `cudaMalloc` 分配；析构时再分别调用 `delete[]` 与 `cudaFree`。

```cpp
class Device {
public:
    TensorDevice device;
    float* space;
    size_t size;

    Device(TensorDevice device, size_t size);
    ~Device();
};
```

直接让每个 Tensor 保存裸指针会遇到两个麻烦：复制对象后，两份对象都可能释放同一地址；若干 Tensor 共享存储时，又很难判断最后一次释放发生在哪里。这里用 `std::shared_ptr<Device>` 托管存储，让底层数据在最后一个引用消失时自动释放。

普通拷贝共享底层存储。跨设备迁移则调用 `deep_copy()`，为目标设备重新分配空间，再根据源设备和目标设备选择复制方向。

| 源设备 | 目标设备 | 复制方式 |
| --- | --- | --- |
| CPU | CPU | `memcpy` |
| CPU | GPU | `cudaMemcpyHostToDevice` |
| GPU | CPU | `cudaMemcpyDeviceToHost` |
| GPU | GPU | `cudaMemcpyDeviceToDevice` |

![Host 与 Device 的协作](assets/slides/02-host-device.png)

Host 与 device 拥有各自的地址空间。`cudaMalloc` 返回的指针只能由 device kernel 直接访问，CPU 侧负责保存这个地址、发起复制和启动计算。于是 `.gpu()` 不能只改 Tensor 的设备标签，它必须先在 device 上分配空间，再执行 host-to-device copy；`.cpu()` 的迁移方向正好相反。

这种区分很重要。若 `.gpu()` 仍与原 CPU Tensor 共用一个普通指针，设备 kernel 会把主机地址当成显存地址；若迁移后仍共享同一 `Device` 对象，`device` 字段也无法同时描述两端的数据。

## Tensor 元数据

Tensor 保存形状、元素总数、所在设备和底层存储。

```cpp
class Tensor {
public:
    std::vector<int> shape;
    TensorDevice device;
    device_ptr data;
    int size;
};
```

多维 Tensor 最终仍落在一段线性内存中，`shape` 只描述各维长度，真正的地址还取决于 stride 与起始偏移。这个 Lab 没有保存 stride，所有数据都按连续行主序解释，因此不能仅修改元数据来表示转置、切片或其他非连续 view。也正因为布局固定，kernel 才能直接用一个线性下标访问全部元素。

![相邻线程的合并访存](assets/slides/02-coalesced-access.png)

逐元素算子让相邻 thread 处理相邻下标，它们对 `in[i]` 与 `out[i]` 的访问也落在连续地址上。一个 warp 的多次请求因而可以合并成较少的显存事务。若 Tensor 支持任意 stride，这个映射就不再天然连续，kernel 还要根据布局重新安排线程与地址。

构造时计算一次各维长度之积，后续 kernel 直接使用 `size`。`.cpu()` 与 `.gpu()` 的规则为：

- 已在目标设备时，返回共享存储的轻量拷贝。
- 需要迁移时，创建目标设备 Tensor，并深拷贝数据。

GPU Tensor 不能在主机端直接解引用。输出运算符遇到 GPU 数据时，先复制到 CPU，再根据 `shape` 递归打印。这个实现适合调试，却不适合频繁出现在训练循环中，因为每次打印都包含一次同步的数据传输。

## CUDA 执行方式

一次 kernel launch 会创建一个 grid，grid 中包含若干 block，每个 block 再包含若干 thread。尖括号中的两个参数分别控制 block 数和每个 block 的 thread 数。

![Kernel 的线程层次](assets/slides/02-kernel-launch.png)

四个 kernel 都使用 grid-stride loop。线程的第一个下标为 `blockIdx.x * blockDim.x + threadIdx.x`，随后以 `blockDim.x * gridDim.x` 为步长继续向后扫描，因此同一份 kernel 能覆盖任意长度的 Tensor。即使以后为了限制 launch 数量而不再按元素数创建足量 block，已有线程也能继续处理剩余元素。

```cpp
#define CUDA_KERNEL_LOOP(i, n)                                      \
    for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < (n);    \
         i += blockDim.x * gridDim.x)
```

block 大小固定为 512，block 数量按元素个数向上取整。kernel 启动后显式调用 `cudaDeviceSynchronize()`，这样函数返回时结果已经写完，调试也更容易定位到当前算子。同步会牺牲流水执行效率，若继续扩展框架，应把同步与错误检查统一放到更高层管理。

## 激活函数

### ReLU

前向计算为

$$
y=\max(x,0)
$$

在 $x=0$ 处按 PyTorch 的定义取零梯度

$$
\frac{\partial L}{\partial x}=
\begin{cases}
\dfrac{\partial L}{\partial y}, & x>0\\
0, & x\leq 0
\end{cases}
$$

CPU 与 GPU 使用完全相同的分支条件。否则零点附近的对照测试会出现不一致。

```cpp
CUDA_KERNEL_LOOP(i, size) {
    out[i] = in[i] > 0 ? grad[i] : 0;
}
```

### Sigmoid

前向计算为

$$
y=\sigma(x)=\frac{1}{1+\exp(-x)}
$$

反向传播可以复用前向值

$$
\frac{\partial L}{\partial x}
=\frac{\partial L}{\partial y}y(1-y)
$$

当前接口只传入原输入与上游梯度，因此反向函数会重新计算一次 Sigmoid。若以后有计算图和前向缓存，可以直接保存 $y$ ，省掉这次指数运算。

## 设备对齐

二元操作收到的两个 Tensor 可能不在同一设备。`onlyDevice()` 使用了一条简单规则：只要其中一个在 GPU，就把另一个也迁移到 GPU；两者都在 CPU 时才执行 CPU 路径。

这能让激活函数的反向接口保持简洁，但它隐含了一次可能很昂贵的复制。更完整的框架通常会拒绝设备不一致的输入，让调用者显式决定数据放在哪里，避免一次拼写失误悄悄触发主机与显卡之间的传输。

## 正确性测试

`main.cu` 构造形状为 $2\times3\times4$ 的 Tensor，输入均匀取自 $[-1,1)$ ，上游梯度使用固定随机种子 1017。测试按以下顺序进行：

1. 将输入从 CPU 复制到 GPU，再复制回来，检查迁移结果。
2. 在 CPU、GPU 上分别执行 ReLU 与 Sigmoid 前向。
3. 传入同一份上游梯度，执行两种激活函数的反向传播。
4. 把 GPU 输出复制回主机，与 CPU 结果逐项比较。

ReLU 的两条路径完全一致。Sigmoid 前向与反向只出现小于 $10^{-7}$ 的末位舍入差异，来自 CPU 与 CUDA 数学函数的浮点实现差别。

还应单独检查三个边界输入：

| 输入 | ReLU 输出 | ReLU 梯度 | Sigmoid 输出 |
| ---: | ---: | ---: | ---: |
| $-1$ | $0$ | $0$ | $0.26894143$ |
| $0$ | $0$ | $0$ | $0.5$ |
| $11/12$ | $11/12$ | 上游梯度 | $0.71436244$ |

## 编译与运行

```bash
nvcc -std=c++17 -Xcompiler=/utf-8 \
  main.cu tensor.cu -o build/lab2.exe
./build/lab2.exe
```

若程序在 kernel 启动后才崩溃，先在每次 CUDA API 调用后检查错误，再保留同步定位出错的算子。等接口稳定后，再考虑去掉逐算子同步、增加异步复制或复用显存。
