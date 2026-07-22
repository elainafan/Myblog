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

## CUDA Tensor简要介绍

Lab 2 要从一个只保存 `float` 的 Tensor 开始，补齐 CPU、GPU 两种存储，再实现 ReLU、Sigmoid 的前向和反向。代码只有三个文件，主要工作是理清存储由谁释放、复制 Tensor 时究竟复制什么，以及 Host 代码能不能直接访问手里的指针。

## 在动手之前

CPU 与 GPU 拥有彼此独立的地址空间。CPU 指针不能直接交给 kernel，GPU 指针也不能在普通 C++ 代码中解引用；跨设备数据必须经过 `cudaMemcpy`，并明确 HostToDevice、DeviceToHost 或 DeviceToDevice 方向。

CUDA kernel 由大量线程执行同一段函数。每个线程根据 block、thread 编号计算自己的线性下标，再判断下标是否越界。元素级激活函数可以让一个线程处理一个元素，block 数由元素总数向上取整得到。kernel launch 默认异步，调试阶段还要检查 launch error 并在读取结果前同步。

Tensor 本身只描述 shape、设备和存储引用。存储对象负责申请与释放内存，Tensor 的普通拷贝共享存储，`.cpu()` 与 `.gpu()` 才执行深拷贝。把生命周期放进构造和析构函数后，函数提前返回时也不会漏掉 `cudaFree()`。

反向函数接收的是上游梯度。ReLU 根据输入是否大于零选择保留或清零，Sigmoid 则把上游梯度乘上 $y(1-y)$ 。两条 CPU 路径先给出数值基准，CUDA kernel 使用完全相同的边界约定。

## 开始动手！

```text
Lab2/
├── tensor.h     Device、device_ptr、Tensor 与 kernel 声明
├── tensor.cu    Tensor 方法、CPU 路径与 CUDA kernel
└── main.cu      固定输入和 CPU/GPU 对照
```

先把存储和复制跑通，再接 Tensor 与算子。`.gpu()` 和 `.cpu()` 尚未验证时，后面的数值错误无法区分是拷贝还是 kernel 所致。

```text
Device 管理一段内存
   ↓
Tensor 保存形状、设备和共享存储
   ↓
算子根据设备分派到 CPU 循环或 CUDA kernel
```

`main.cu` 不碰裸指针之外的实现细节。它构造一个 $2\times3\times4$ Tensor，依次跑 CPU 与 GPU 的前向、反向，再把结果打印出来对照。

### 存储层

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

构造函数只做分配，不做初始化。新建输出 Tensor 后，CPU 循环或 kernel 必须覆盖其中每个元素；若某条分支漏写，打印出来的并不是固定的零，而是未初始化内存。输出每次运行都变化时，先检查是否完整写入。

`device_ptr` 以 `std::shared_ptr<Device>` 为基础。普通 Tensor 拷贝只增加引用计数，共享同一段存储；跨设备迁移则调用 `deep_copy()`，在目标设备重新分配空间，再选择对应的复制方向。

| 源 | 目标 | 复制方式 |
| --- | --- | --- |
| CPU | CPU | `memcpy` |
| CPU | GPU | `cudaMemcpyHostToDevice` |
| GPU | CPU | `cudaMemcpyDeviceToHost` |
| GPU | GPU | `cudaMemcpyDeviceToDevice` |

这里要有意识地区分浅拷贝和深拷贝。若每次复制 Tensor 都复制显存，传参成本会很高；若 `.gpu()` 只修改设备标签，kernel 又会把主机地址当成显存地址。共享存储用于同设备的对象语义，深拷贝用于真正的数据迁移，二者不能混用。

```cpp
Tensor::Tensor(const Tensor& other)
    : device(other.device),
      shape(other.shape),
      data(other.data),
      size(other.size) {}
```

这里复制的是 `device_ptr`。两个 Tensor 的 `data->space` 指向同一块内存，最后一个引用离开作用域时才释放。于是普通复制很轻，但也带来别名问题：以后若加入原地赋值，改动其中一个 Tensor 会同时改变另一个 Tensor 看到的数据。

`deep_copy()` 则先按目标设备分配新空间，再根据源、目标的组合选择 `memcpy` 或 `cudaMemcpy`。四种方向都单独列出来，能避免把 `cudaMemcpyHostToDevice` 的参数顺序凭感觉写反。

![Host 与 Device 的分工](assets/slides/02-host-device.png)

### Tensor 层

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

构造时还要处理 shape 的边界。空 shape 可以表示标量，此时元素数应为 1；任一维为 0 时，元素数为 0；负维度则应在分配前拒绝。当前实验只传入正维度，因此源码没有把这些检查全部补齐，但接口扩展后不能继续默认调用端永远正确。

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

这里会先由 `Tensor result(...)` 分配一块显存，随后 `result.data` 又被 `deep_copy()` 返回的新存储覆盖。旧存储会因智能指针失去引用而释放，结果正确，却多做了一次分配。若继续整理接口，可以让 Tensor 接受一份已经构造好的 `device_ptr`，或者让迁移函数直接填入既有目标空间。

打印函数很适合调试，却不应放进训练热路径。一次 `std::cout << gpu_tensor` 隐含了同步的 device-to-host copy，循环里频繁打印会让时间几乎都花在传输和等待上。

### 算子分派

ReLU 和 Sigmoid 的公开接口都放在 Tensor 上。函数先创建同形状输出，再根据 `device` 选择普通循环或 CUDA kernel。

```text
Tensor::relu_cpu_forward()
├── CPU：for 循环
└── GPU：Kernel::relu_gpu_forward<<<...>>>()
```

函数名中虽然保留了 `cpu`，实际已经承担统一分派职责。若继续扩充框架，改成 `relu_forward()` 会更符合接口含义，后端选择仍留在函数内部。

反向算子有两个输入：前向输入和上游梯度。`onlyDevice()` 先把它们对齐到同一设备，只要其中一个在 GPU，另一个也会迁移到 GPU。这个策略让调用端简单，却可能悄悄产生昂贵的数据复制。规模更大的框架通常直接拒绝设备不一致的输入，让调用者显式决定迁移时机。

源码中四种组合对应四条调用路径。

| `in` | `grad` | 计算位置 | 隐含复制 |
| --- | --- | --- | --- |
| CPU | CPU | CPU | 无 |
| GPU | CPU | GPU | `grad` 搬到 GPU |
| CPU | GPU | GPU | `in` 搬到 GPU |
| GPU | GPU | GPU | 无 |

统一分派省掉了调用端分支，也让一次误传的 CPU 梯度悄悄触发 H2D copy。后面训练网络时，这种便利会掩盖性能问题，因此测试接口和训练接口未必要采用同一策略。

### CUDA kernel

逐元素算子使用 grid-stride loop。每个线程先处理自己的线性下标，再以整个 grid 的线程总数为步长继续向后扫描。

```cpp
#define CUDA_KERNEL_LOOP(i, n)                                      \
    for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < (n);    \
         i += blockDim.x * gridDim.x)
```

![Kernel 的线程层次](assets/slides/02-kernel-launch.png)

这种写法把“输入有多少元素”和“本次启动多少线程”分开，同一个 kernel 可以覆盖任意长度。线性下标还让相邻线程访问相邻元素，显存请求更容易合并。

每个 block 使用 512 个线程，block 数由向上取整得到。

```cpp
const int kCudaThreadsNum = 512;

inline int CudaGetBlocks(int n) {
    return (n + kCudaThreadsNum - 1) / kCudaThreadsNum;
}
```

即使 block 数已经足以覆盖全部元素，grid-stride loop 仍然保留。以后若人为限制 grid 大小，kernel 也不需要改写；输入末尾不足一个 block 的部分则由 `i < n` 拦住。

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

### CPU 与 GPU 对照

`main.cu` 先在 CPU 上生成从负数逐渐过渡到正数的输入，再调用 `.gpu()`。这种输入比全随机数更适合检查 ReLU，因为负区间、零附近与正区间能同时出现。上游梯度使用固定随机种子生成，CPU、GPU 的反向过程读的是同一份数值。

```cpp
Tensor input_gpu = build_test_tensor_gpu();
Tensor input_cpu = input_gpu.cpu();
Tensor grad = random_cpu_tensor(input_gpu.shape);

Tensor relu_gpu = input_gpu.relu_cpu_forward();
Tensor relu_cpu = input_cpu.relu_cpu_forward();
```

测试先打印 `input_gpu.cpu()`，确认往返复制没有改变数据；随后比较前向，最后比较反向。第一步已经出错时，问题仍在存储或复制路径，尚未进入激活函数。

当前代码通过打印人工比较，适合小 Tensor。更可靠的版本应增加 `allclose`，逐元素检查绝对误差与相对误差，并在失败时输出第一个不一致下标。Tensor 变大以后，肉眼看两屏数字几乎发现不了单个错误。

### 调试时踩过的坑

- GPU 指针只能由设备代码直接解引用。Host 端若要查看数据，必须先复制到 CPU。
- kernel launch 是异步的。当前实现用 `cudaDeviceSynchronize()` 便于定位错误，但每个算子都同步会切断流水执行。
- 只同步还不够。调试时应同时检查 kernel launch 和 CUDA API 的错误码，否则错误可能拖到后一次调用才暴露。
- 二元算子不能只检查元素总数，还要检查形状是否兼容。两个 `size` 相同的 Tensor 不一定具有相同语义。
- 共享存储意味着一份数据可能有多个 Tensor 引用。以后加入原地写入时，需要明确它会不会同时改变其他别名。

`cudaDeviceSynchronize()` 只负责等待 kernel 完成，返回值仍要检查。若 launch 配置非法，错误可能在同步处才暴露；若前面的 `cudaMemcpy` 已经失败，后续 kernel 报出的地址错误又只是连锁反应。分配、复制和 launch 三个边界应分别检查 CUDA 状态。

### 成品代码

最终版本由 `tensor.h`、`tensor.cu` 和 `main.cu` 组成，完整代码见 [Lab 2 源码](https://github.com/elainafan/Programming-in-AI-2025Fall-PKU/tree/main/Lab2)。三个文件的边界保持不变：头文件声明接口，CUDA 源文件管理存储与算子，测试入口只通过 Tensor 的公开方法构造和比较结果。

提交前要确认普通 Tensor 拷贝不会重复释放内存，`.cpu()` 与 `.gpu()` 不会只改设备标签，所有输出 Tensor 都被完整写入。`main.cu` 中不应直接读取 GPU 指针。

### 正确性验证

`main.cu` 构造固定的 $2\times3\times4$ 输入和上游梯度，先检查 CPU/GPU 往返复制，再比较两种激活函数的前向与反向结果。ReLU 还应单独覆盖负数、零和正数三个边界，Sigmoid 则要补一个绝对值较大的输入，观察指数计算是否溢出。

```bash
nvcc -std=c++17 -Xcompiler=/utf-8 \
  main.cu tensor.cu -o build/lab2.exe
./build/lab2.exe
```

CPU 与 GPU 之间往返复制后，打印值完全一致。确定性输入中，Sigmoid 在 $-1$ 、 $0$ 和 $11/12$ 处的输出分别为 0.26894143、0.5 和 0.71436244；ReLU 在非正输入处的输出与梯度均为零。CPU 与 CUDA 路径采用了相同的边界约定。

两条路径只出现浮点末位差异时，再检查误差阈值；若整段输出错位，则先查 shape、复制方向和 kernel 下标。CPU 路径负责提供数值基准，CUDA 每增加一步都先与它对照，再继续接下一个算子。
