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

## CUDA Tensor 简要介绍

Lab 2 要从一个只保存 `float` 的 Tensor 开始，补齐 CPU、GPU 两种存储，再实现 ReLU、Sigmoid 的前向和反向。代码只有三个文件，内容集中在存储的释放、Tensor 的复制语义，以及 Host 与 Device 指针的访问范围。

## 在动手之前

CPU 与 GPU 拥有彼此独立的地址空间。CPU 指针不能直接交给 kernel，GPU 指针也不能在普通 C++ 代码中解引用；跨设备数据必须经过 `cudaMemcpy`，并明确 HostToDevice、DeviceToHost 或 DeviceToDevice 方向。

CUDA kernel 由大量线程执行同一段函数。每个线程根据 block、thread 编号计算自己的线性下标，再判断下标是否越界。元素级激活函数可以让一个线程处理一个元素，block 数由元素总数向上取整得到。kernel launch 默认异步，调试阶段还要检查 launch error 并在读取结果前同步。

Tensor 本身只描述 shape、设备和存储引用。存储对象负责申请与释放内存，Tensor 的普通拷贝共享存储，`.cpu()` 与 `.gpu()` 才执行深拷贝。把生命周期放进构造和析构函数后，函数提前返回时也不会漏掉 `cudaFree()`。

反向函数接收上游梯度。ReLU 根据输入是否大于零选择保留或清零，Sigmoid 则把上游梯度乘上 $y(1-y)$ 。CPU 与 CUDA 路径在 $x=0$ 处采用同一套规则。

## 开始动手！

```text
Lab2/
├── tensor.h     Device、device_ptr、Tensor 与 kernel 声明
├── tensor.cu    Tensor 方法、CPU 路径与 CUDA kernel
└── main.cu      固定输入和 CPU/GPU 对照
```

实现从存储和复制开始。`main.cu` 先检查 `.gpu()`、`.cpu()` 的往返结果，再运行激活函数；这样第一次出现数值差异的位置就是出错的调用。

`main.cu` 只在构造 CPU 测试数据时直接写 `data->space`，其余步骤都调用 Tensor 接口。它构造一个 $2\times3\times4$ Tensor，依次跑 CPU 与 GPU 的前向、反向，再把结果打印出来对照。

### Device 与内存

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

构造函数只做分配，不做初始化。新建输出 Tensor 后，CPU 循环或 kernel 必须覆盖其中每个元素；若某条分支漏写，打印出来的就是未初始化内存。输出每次运行都变化时，先检查是否完整写入。

`device_ptr` 以 `std::shared_ptr<Device>` 为基础。普通 Tensor 拷贝只增加引用计数，共享同一段存储；跨设备迁移则调用 `deep_copy()`，在目标设备重新分配空间，再选择对应的复制方向。

| 源 | 目标 | 复制方式 |
| --- | --- | --- |
| CPU | CPU | `memcpy` |
| CPU | GPU | `cudaMemcpyHostToDevice` |
| GPU | CPU | `cudaMemcpyDeviceToHost` |
| GPU | GPU | `cudaMemcpyDeviceToDevice` |

```cpp
Tensor::Tensor(const Tensor& other)
    : device(other.device),
      shape(other.shape),
      data(other.data),
      size(other.size) {}
```

这里复制的是 `device_ptr`。两个 Tensor 的 `data->space` 指向同一块内存，最后一个引用离开作用域时才释放。普通复制很轻，但两个对象看到的也是同一份数据。

`deep_copy()` 则先按目标设备分配新空间，再根据源、目标的组合选择 `memcpy` 或 `cudaMemcpy`。四种方向都单独列出来，能避免把 `cudaMemcpyHostToDevice` 的参数顺序凭感觉写反。

![Host 与 Device 的分工](assets/slides/02-host-device.png)

### Tensor

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

构造函数计算各维长度之积，逐元素 kernel 直接使用 `size`。当前 Tensor 没有 stride 和 offset，所有数据都按连续行主序解释。

`.cpu()` 与 `.gpu()` 是 Tensor 层的设备入口。已经位于目标设备时，返回共享存储的轻量拷贝；需要迁移时，才通过存储层做深拷贝。GPU Tensor 的打印也复用 `.cpu()`，先把数据搬回主机，再按 `shape` 递归输出。

```cpp
Tensor Tensor::gpu() const {
    if (device == TensorDevice::GPU) return Tensor(*this);

    Tensor result(shape, TensorDevice::GPU);
    result.data = data.deep_copy(TensorDevice::GPU);
    result.size = size;
    return result;
}
```

这里会先由 `Tensor result(...)` 分配一块显存，随后 `result.data` 又被 `deep_copy()` 返回的新存储覆盖。旧存储会因智能指针失去引用而释放，结果正确，不过多做了一次分配。

一次 `std::cout << gpu_tensor` 会先把数据复制回 CPU，因此打印函数只在这份小规模测试中使用。

### 设备分派

ReLU 和 Sigmoid 的入口都放在 Tensor 上。函数先创建同形状输出，再根据 `device` 进入普通循环或 CUDA kernel。函数名虽然保留了 `_cpu_forward`，实际计算位置仍由输入 Tensor 的设备决定。

反向算子有两个输入：前向输入和上游梯度。`onlyDevice()` 先把它们对齐到同一设备，只要其中一个在 GPU，另一个也会迁移到 GPU。

源码中四种组合对应四条调用路径。

| `in` | `grad` | 计算位置 | 隐含复制 |
| --- | --- | --- | --- |
| CPU | CPU | CPU | 无 |
| GPU | CPU | GPU | `grad` 搬到 GPU |
| CPU | GPU | GPU | `in` 搬到 GPU |
| GPU | GPU | GPU | 无 |

传入不同设备的两个 Tensor 不会直接报错，而是多发生一次 H2D copy。调试反向函数时要把这次隐含复制算进去。

### CUDA kernel

逐元素算子使用 grid-stride loop。每个线程先处理自己的线性下标，再以整个 grid 的线程总数为步长继续向后扫描。

```cpp
#define CUDA_KERNEL_LOOP(i, n)                                      \
    for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < (n);    \
         i += blockDim.x * gridDim.x)
```

![Kernel 的线程层次](assets/slides/02-kernel-launch.png)

grid-stride loop 不要求线程总数等于元素数，同一个 kernel 可以覆盖任意长度。线性下标还让相邻线程访问相邻元素，显存请求更容易合并。

每个 block 使用 512 个线程，block 数由向上取整得到。

```cpp
const int kCudaThreadsNum = 512;

inline int CudaGetBlocks(int n) {
    return (n + kCudaThreadsNum - 1) / kCudaThreadsNum;
}
```

输入末尾不足一个 block 的部分由 `i < n` 拦住，grid-stride loop 则负责继续处理超过当前 grid 覆盖范围的元素。

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

当前反向 kernel 会重新计算一次 $y$ ，没有保存前向输出。

### 对照与调试

`main.cu` 先在 CPU 上生成从负数逐渐过渡到正数的输入，再调用 `.gpu()`。这种输入比全随机数更适合检查 ReLU，因为负区间、零附近与正区间能同时出现。上游梯度使用固定随机种子生成，CPU、GPU 的反向过程读的是同一份数值。

```cpp
Tensor input_gpu = build_test_tensor_gpu();
Tensor input_cpu = input_gpu.cpu();
Tensor grad = random_cpu_tensor(input_gpu.shape);

Tensor relu_gpu = input_gpu.relu_cpu_forward();
Tensor relu_cpu = input_cpu.relu_cpu_forward();
```

测试先打印 `input_gpu.cpu()`，确认往返复制没有改变数据；随后比较前向，最后比较反向。第一步已经出错时，问题仍在存储或复制路径，尚未进入激活函数。

当前代码通过打印结果进行比较，因此测试 Tensor 刻意取得很小。

Host 端打印 GPU Tensor 时会先调用 `.cpu()`，所以打印正常只能说明 D2H copy 和输出格式正常。kernel launch 默认异步，源码在算子后调用 `cudaDeviceSynchronize()`，越界等错误会在这里暴露。同步本身也有返回值，`cudaMalloc`、`cudaMemcpy` 和 launch error 仍需分别检查，否则前一次复制失败可能拖到后一个 kernel 才报出来。

### 成品代码

最终版本由 `tensor.h`、`tensor.cu` 和 `main.cu` 组成。头文件声明 Device、Tensor 与 kernel，CUDA 源文件实现存储和算子，`main.cu` 构造固定输入并打印 CPU、GPU 结果。完整代码见 [Lab 2 源码](https://github.com/elainafan/Programming-in-AI-2025Fall-PKU/tree/main/Lab2)。

### 正确性验证

`main.cu` 构造固定的 $2\times3\times4$ 输入和上游梯度，先检查 CPU/GPU 往返复制，再比较两种激活函数的前向与反向结果。输入从负数逐渐过渡到正数，ReLU 的两个分支都能在同一次运行中出现。

```bash
nvcc -std=c++17 -Xcompiler=/utf-8 \
  main.cu tensor.cu -o build/lab2.exe
./build/lab2.exe
```

CPU 与 GPU 之间往返复制后，打印值完全一致。确定性输入中，Sigmoid 在 $-1$ 、 $0$ 和 $11/12$ 处的输出分别为 0.26894143、0.5 和 0.71436244；ReLU 在非正输入处的输出与梯度均为零。CPU 与 CUDA 路径采用了相同的边界约定。
