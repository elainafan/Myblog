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

Lab 2 从一个只保存 `float` 的 Tensor 开始，补齐 CPU、GPU 两种存储，以及 ReLU、Sigmoid 的前向和反向计算。实现分为三个层次。

```text
Device 管理一段内存
   ↓
Tensor 保存形状、设备和共享存储
   ↓
算子根据设备分派到 CPU 循环或 CUDA kernel
```

`main.cu` 位于最上层，只构造输入并对照两条执行路径。这样内存生命周期、Tensor 语义、算子计算和测试不会挤在同一层里。

## 存储层

`Device` 只负责一段连续存储。CPU 端用 `new[]` 与 `delete[]`，GPU 端用 `cudaMalloc` 与 `cudaFree`。设备类型、首地址和元素数都封装在同一个对象中。

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

内存的申请和释放在构造、析构函数中成对出现。上层即使提前返回或抛出异常，栈展开仍会触发析构，这比在每个算子末尾手动释放可靠得多。

`device_ptr` 以 `std::shared_ptr<Device>` 为基础。普通 Tensor 拷贝只增加引用计数，共享同一段存储；跨设备迁移则调用 `deep_copy()`，在目标设备重新分配空间，再选择对应的复制方向。

| 源 | 目标 | 复制方式 |
| --- | --- | --- |
| CPU | CPU | `memcpy` |
| CPU | GPU | `cudaMemcpyHostToDevice` |
| GPU | CPU | `cudaMemcpyDeviceToHost` |
| GPU | GPU | `cudaMemcpyDeviceToDevice` |

这里要有意识地区分浅拷贝和深拷贝。若每次复制 Tensor 都复制显存，传参成本会很高；若 `.gpu()` 只修改设备标签，kernel 又会把主机地址当成显存地址。共享存储用于同设备的对象语义，深拷贝用于真正的数据迁移，二者不能混用。

![Host 与 Device 的分工](assets/slides/02-host-device.png)

## Tensor 层

Tensor 不直接负责释放内存，只保存元数据和指向存储对象的智能指针。

```cpp
class Tensor {
public:
    std::vector<int> shape;
    TensorDevice device;
    device_ptr data;
    int size;
};
```

构造函数计算一次各维长度之积，后续逐元素 kernel 直接使用 `size`。当前实现没有 stride 和 offset，所有 Tensor 都按连续行主序解释。因此 reshape、转置、切片等操作还不能只靠修改元数据完成；它们需要增加布局信息，或者重新整理数据。

`.cpu()` 与 `.gpu()` 是 Tensor 层的设备入口。已经位于目标设备时，返回共享存储的轻量拷贝；需要迁移时，才通过存储层做深拷贝。GPU Tensor 的打印也复用 `.cpu()`，先把数据搬回主机，再按 `shape` 递归输出。

打印函数很适合调试，却不应放进训练热路径。一次 `std::cout << gpu_tensor` 隐含了同步的 device-to-host copy，循环里频繁打印会让时间几乎都花在传输和等待上。

## 算子分派

ReLU 和 Sigmoid 的公开接口都放在 Tensor 上。函数先创建同形状输出，再根据 `device` 选择普通循环或 CUDA kernel。

```text
Tensor::relu_cpu_forward()
├── CPU：for 循环
└── GPU：Kernel::relu_gpu_forward<<<...>>>()
```

函数名中虽然保留了 `cpu`，实际已经承担统一分派职责。若继续扩充框架，改成 `relu_forward()` 会更符合接口含义，后端选择仍留在函数内部。

反向算子有两个输入：前向输入和上游梯度。`onlyDevice()` 先把它们对齐到同一设备，只要其中一个在 GPU，另一个也会迁移到 GPU。这个策略让调用端简单，却可能悄悄产生昂贵的数据复制。规模更大的框架通常直接拒绝设备不一致的输入，让调用者显式决定迁移时机。

## CUDA kernel

逐元素算子使用 grid-stride loop。每个线程先处理自己的线性下标，再以整个 grid 的线程总数为步长继续向后扫描。

```cpp
#define CUDA_KERNEL_LOOP(i, n)                                      \
    for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < (n);    \
         i += blockDim.x * gridDim.x)
```

![Kernel 的线程层次](assets/slides/02-kernel-launch.png)

这种写法把“输入有多少元素”和“本次启动多少线程”分开，同一个 kernel 可以覆盖任意长度。线性下标还让相邻线程访问相邻元素，显存请求更容易合并。

![相邻线程的合并访存](assets/slides/02-coalesced-access.png)

ReLU 前向和反向分别为

$$
y=\max(x,0)
$$

$$
\frac{\partial L}{\partial x}=
\begin{cases}
\dfrac{\partial L}{\partial y}, & x>0,\\
0, & x\leq0.
\end{cases}
$$

CPU、GPU 在 $x=0$ 处必须采用同一约定，否则边界测试会不一致。

Sigmoid 反向重新计算前向值

$$
y=\frac{1}{1+\exp(-x)}
$$

$$
\frac{\partial L}{\partial x}
=\frac{\partial L}{\partial y}y(1-y)
$$

等框架拥有计算图后，可以缓存 $y$ 并在反向时复用，省去一次指数运算。这个例子也说明前向缓存应由计算图或算子节点管理，不宜随意塞进 Tensor 存储层。

## 写的时候容易踩的坑

- GPU 指针只能由设备代码直接解引用。Host 端若要查看数据，必须先复制到 CPU。
- kernel launch 是异步的。当前实现用 `cudaDeviceSynchronize()` 便于定位错误，但每个算子都同步会切断流水执行。
- 只同步还不够。调试时应同时检查 kernel launch 和 CUDA API 的错误码，否则错误可能拖到后一次调用才暴露。
- 二元算子不能只检查元素总数，还要检查形状是否兼容。两个 `size` 相同的 Tensor 不一定具有相同语义。
- 共享存储意味着一份数据可能有多个 Tensor 引用。以后加入原地写入时，需要明确它会不会同时改变其他别名。

这些问题分别属于存储、执行和接口层。把它们混在 kernel 内处理，最后往往只剩下一串难以定位的 CUDA 错误。

## 复验

`main.cu` 构造固定的 $2\times3\times4$ 输入和上游梯度，先检查 CPU/GPU 往返复制，再比较两种激活函数的前向与反向结果。ReLU 还应单独覆盖负数、零和正数三个边界。

```bash
nvcc -std=c++17 -Xcompiler=/utf-8 \
  main.cu tensor.cu -o build/lab2.exe
./build/lab2.exe
```

两条路径只出现浮点末位差异时，可以把问题收窄到数学库实现；若整段输出错位，则优先检查形状、复制方向和 kernel 下标。这样的对照比只看一份 GPU 输出更容易找到模块边界上的错误。
