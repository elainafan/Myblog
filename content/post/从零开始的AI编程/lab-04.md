---
title: 从零开始的 Python 扩展
date: 2025-11-25
categories:
    - AI
slug: ai-programming-lab-04
hidden: true
seriesOrder: 24
---

# 从零开始的 Python 扩展

> [!CAUTION]
>
> **本笔记仅供参考，请勿抄袭。**

## Python 扩展简要介绍

前三次 Lab 的 CUDA Tensor 只能由 C++ 调用。Lab 4 用 pybind11 把它编译成 `mytensor`，Python 端要能创建 Tensor、与 NumPy 交换数据，并调用前面写好的神经网络算子。

这一份没有多少新公式，工作集中在 Python 与 C++ 的接口上。dtype、连续性、返回对象的生命周期和 CUDA 报错位置中，任何一处处理错了，都可能表现为 `import` 失败、段错误或随机数值。

## 在动手之前

pybind11 负责在 Python 对象与 C++ 类型之间转换。模块由 `PYBIND11_MODULE` 注册，编译结果必须与当前 Python 的 ABI、架构和运行库匹配；文件能生成并不代表一定能被 `import`。

NumPy 数组除了数据首地址，还带有 dtype、shape、stride 和所有权信息。C++ 后端要求连续的 `float32` 数据时，绑定层必须显式检查或转换。返回数组时也要保证底层内存在 Python 对象存活期间一直有效，不能把局部缓冲区包装成悬空 view。

Python 异常适合报告 shape、dtype 和参数范围错误，CUDA 错误则应尽量在 binding 返回前检查。kernel 异步执行时，越界可能拖到 `.numpy()` 或下一次 CUDA API 调用才出现，因此导入、数据转换和数值计算要分层测试。

## 开始动手！

Python 代码只接触 `mytensor` 暴露出的对象。`tensornn.cu` 负责参数转换，底层 CUDA 函数仍然只接收指针与 shape。

### 文件结构

```text
Lab4/
├── data/
│   └── mnist.py
├── src/
│   ├── CMakeLists.txt
│   ├── tensor.cu
│   ├── tensor.h
│   ├── tensor_kernel.h
│   └── tensornn.cu
└── test/
    ├── conftest.py
    ├── test_conv.py
    ├── test_cross_entropy.py
    ├── test_full_connect.py
    ├── test_maxpool.py
    ├── test_relu.py
    ├── test_sigmoid.py
    └── test_softmax.py
```

`tensor.*` 与 `tensor_kernel.h` 保存 CUDA 实现，`tensornn.cu` 注册 Python 接口，`data/` 和 `test/` 只导入编译后的模块。CMake 把这些源文件编译成 `mytensor.pyd`。

### 编译 mytensor

`CMakeLists.txt` 同时启用 C++20 与 CUDA 20，再依次查找 Python、pybind11 和 CUDA Toolkit。

```cmake
project(Lab4 LANGUAGES CXX CUDA)

find_package(
    Python 3.8
    COMPONENTS Interpreter Development.Module
    REQUIRED
)
find_package(CUDAToolkit REQUIRED)

pybind11_add_module(mytensor tensor.cu tensornn.cu)
target_link_libraries(
    mytensor PRIVATE CUDA::cublas CUDA::curand
)
```

这里不能只找到任意一个 Python。CMake 用哪个解释器和开发库编译，测试就应由同一套 ABI 的解释器导入。pybind11 没有被 CMake 直接找到时，脚本会执行 `python -m pybind11 --cmakedir`，再把返回目录加入 `CMAKE_PREFIX_PATH`。

Windows 的 Release 构建产物位于 `build/Release/mytensor.pyd`。`conftest.py` 在测试开始前把 `build/Release` 和 `build` 加入 `sys.path`，并用 `os.add_dll_directory()` 注册 CUDA 的 `bin` 目录。`.pyd` 已经生成却仍然导入失败时，问题通常在依赖 DLL 或 Python ABI。

### Tensor 绑定

`PYBIND11_MODULE` 注册设备枚举、Tensor 类和 `nn` 子模块。

```cpp
PYBIND11_MODULE(mytensor, m) {
    py::enum_<TensorDevice>(m, "TensorDevice")
        .value("CPU", TensorDevice::CPU)
        .value("GPU", TensorDevice::GPU);

    py::class_<Tensor>(m, "Tensor")
        .def(py::init<const std::vector<int>&, TensorDevice>())
        .def("shape", &Tensor::getShape)
        .def("cpu", &Tensor::cpu)
        .def("gpu", &Tensor::gpu)
        .def("numpy", &tensor2numpy)
        .def_static("from_numpy", &numpy2tensor);

    auto nn = m.def_submodule("nn");
}
```

Python 端的调用顺序固定为创建、迁移、计算和回传。

```python
array = np.random.randn(2, 3).astype(np.float32)
tensor = mytensor.Tensor.from_numpy(array)
output = tensor.relu_forward()
result = output.numpy()
```

激活函数作为 Tensor 方法，卷积、池化和全连接等多输入操作放在 `mytensor.nn`，调用时可以直接看出每个算子接收了哪些 Tensor 和参数。

绑定层还给 Tensor 定义了 `__repr__()`，只显示 shape 和 device，不把数据自动搬回 CPU。

```text
<Tensor shape=[2, 3] on GPU>
```

若 `repr` 顺手调用 `.numpy()`，在调试器或 Notebook 中查看变量也会触发同步和 D2H copy。元数据可以随时打印，真实数据则由调用者明确请求。

### NumPy 桥接

`Tensor.from_numpy()` 接收 C-contiguous 的 `float32` 数组。`forcecast` 会把其他可转换类型或非连续 view 整理成所需布局。

```cpp
Tensor numpy2tensor(
    py::array_t<float,
        py::array::c_style | py::array::forcecast> array);
```

绑定函数读取 `ndim` 和 `shape`，创建对应 Tensor，再复制连续数据。`numpy()` 走相反方向：先创建由 NumPy 管理的新数组，再把 CPU 或 GPU Tensor 的内容复制进去。

每一维先从 `py::ssize_t` 转成 `int`。源码在转换前检查是否超过 `int` 上限，避免大数组维度静默截断；Tensor 的底层 shape 仍然使用 `int`，因此这个限制属于公开接口的一部分。

`from_numpy()` 当前总是创建 GPU Tensor。即使传入的是普通 NumPy 数组，返回对象也已经完成 H2D copy；若机器没有可用 CUDA，转换阶段便会失败。这种约定让后面的算子入口简单，却也意味着 `from_numpy()` 不是一个纯粹的数据包装函数。

这里采用双向复制，没有共享存储。Python 数组释放后，Tensor 不会悬空；Tensor 析构后，已经返回的 NumPy 数组仍然有效。

数据复制集中在 `from_numpy()` 和 `numpy()`。算子之间直接传 Tensor，不会在每层前向中往返 Host 与 Device。

标签也经过同一个 `float32` Tensor 通道。Python 测试传入整数标签时，`forcecast` 会把它转换成 `float`，CUDA kernel 再把数值当作类别编号比较。

### 神经网络算子

每个 wrapper 按这个顺序调用后端。

1. 解析 Python 参数并检查维数。
2. 根据输入和 stride、padding 等参数计算输出形状。
3. 分配输出 Tensor。
4. 把底层指针与标量参数交给 CUDA 实现。

卷积接口需要确认输入和权重都是四维、通道数一致、输出高宽为正，再启动 kernel。当前 wrapper 会直接读取 `image.getShape()[3]` 等固定位置；维度不足时，检查还没来得及抛出 Python 异常，C++ 已经越界访问。

全连接和卷积的反向接口都按照输入、权重、偏置的顺序返回梯度。

```cpp
return std::make_tuple(
    input_grad,
    weight_grad,
    bias_grad
);
```

Python 端可以直接写

```python
dx, dw, db = mytensor.nn.conv_backward(
    x, weight, output_grad, 1, 1, 1, 1
)
```

把 `dw` 与 `db` 调换不会在绑定层报错，错误会一直传到后面的计算图中。

| 模块 | Python 输入 | 返回值 |
| --- | --- | --- |
| 激活函数 | 输入、上游梯度 | 输出或输入梯度 |
| 全连接 | 输入、权重、偏置 | 输出或三类梯度 |
| 卷积 | 输入、权重、偏置、步长与填充 | 输出或三类梯度 |
| 最大池化 | 输入、核大小与步长 | 输出或输入梯度 |
| 分类损失 | logits、标签 | 概率、损失或 logits 梯度 |

### MNIST 数据

`data/mnist.py` 只验证数据能经过 NumPy 进入自定义 Tensor，没有在本 Lab 训练网络。

```python
images = dataset.data.numpy().astype(np.float32) / 255.0
images = images[:, None, :, :]
tensor = mytensor.Tensor.from_numpy(images)
```

脚本逐个迭代 Dataset，因此 `ToImage`、转为 `float32` 和归一化都会执行，再由 `np.array` 拼成 batch。这一部分只检查数据能否进入自定义 Tensor，没有参与网络训练。

### 与 PyTorch 对拍

单元测试从同一份 NumPy 随机输入出发，一份交给 PyTorch，一份交给 `mytensor`。反向测试还要传入相同的上游梯度。

```python
expected = torch.nn.functional.relu(torch_input)
actual = custom_input.relu_forward().numpy()

np.testing.assert_allclose(
    actual, expected.numpy(), rtol=1e-5, atol=1e-5
)
```

通过公开接口比较输入输出属于黑盒测试。它会同时经过参数解析、NumPy 复制、CUDA kernel 和结果回传。

![黑盒测试从公开接口检查输入输出](assets/slides/08-black-box-test.png)

另一组用例针对内部边界设计：非方形卷积检查高宽顺序，末尾不足一个 block 的输入检查越界保护，大 logits 检查 Softmax 的稳定化，池化反向检查梯度落点。这些属于白盒测试。

![白盒测试覆盖实现中的分支与路径](assets/slides/08-white-box-test.png)

普通随机输入用于对拍数值，另外几组特制输入负责覆盖高宽顺序、block 尾部和数值稳定性。

反向对拍必须使用同一份上游梯度。若 PyTorch 端对 `output.sum()` 调 `backward()`，自定义端却传随机 `output_grad`，两边求的不是同一个 vector-Jacobian product，结果当然无法比较。

卷积测试还要把 NCHW 和权重布局固定下来。PyTorch 的权重 shape 是 $K\times C\times K_H\times K_W$ ，恰好与当前 CUDA 后端一致；只比较方形输入会掩盖 $H$ 、 $W$ 交换，因此测试中应保留非方形 kernel 或 feature map。

max-pool 的 binding 在本次补上了 batch 维，并在反向前显式清零 `input_grad`。

```cpp
cudaMemset(
    input_grad.getRawData(),
    0,
    input_grad.size * sizeof(float)
);
```

反向 kernel 使用 `+=`，没有这一步就会在未初始化显存上累计。

### 构建与调试

调试顺序从 `import mytensor` 开始。模块能导入后，用一个 $2\times3$ 数组检查 `from_numpy()` 与 `numpy()`；往返结果一致后，再运行各个算子的 pytest。这样 `.pyd`、DLL 和 ABI 问题不会与 CUDA 数值错误混在一起。

`forcecast` 可能为 dtype 或布局不符的数组创建副本，返回 NumPy 时则由 Python 持有一块新的内存。CUDA kernel 的错误有时会拖到 `.numpy()` 同步时才出现，因此 wrapper 返回前还要检查当前 launch 的状态。

### 成品代码

最终代码分为 `src/`、`data/` 和 `test/` 三部分。`src/tensornn.cu` 注册 Python 接口，`src/tensor*` 保留 CUDA 实现，测试文件只依赖构建出的 `mytensor` 模块。完整版本见 [Lab 4 源码](https://github.com/elainafan/Programming-in-AI-2025Fall-PKU/tree/main/Lab4)。

### 测试结果

```powershell
cmake -S src -B build
cmake --build build --config Release

$env:PYTHONPATH = "$(Resolve-Path build/Release)"
python -m pytest -q test
```

当前 13 项测试全部通过，覆盖激活函数、全连接、卷积、池化、Softmax 与交叉熵的前后向。

![](assets/labs/lab-04/pytest.png)
