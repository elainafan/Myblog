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

## 任务

前三次 Lab 的 CUDA Tensor 只能由 C++ 调用。Lab 4 用 pybind11 把它编译成 `mytensor`，Python 端要能创建 Tensor、与 NumPy 交换数据，并调用前面写好的神经网络算子。

本次几乎没有新公式，工作量都在边界上。Python 数组是什么 dtype，内存是否连续，C++ 返回对象由谁持有，CUDA 错误在哪一次调用暴露，任何一处约定含糊都会变成 `import` 失败、段错误或者一组看似随机的数值。

```text
Python / NumPy
      ↓ pybind11
Tensor 接口与形状检查
      ↓
CUDA 算子与显存
```

Python 只接触公开对象。绑定层把 Python 参数翻译为 Tensor 和标量，底层 CUDA 代码仍然只接收指针与 shape。

## 项目分层

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

`tensor.*` 与 `tensor_kernel.h` 是计算后端；`tensornn.cu` 是唯一的 Python 边界；`data/` 和 `test/` 都只通过扩展的公开接口工作。CMake 则把 C++、CUDA、pybind11 和 Python ABI 组装成可导入的 `.pyd`。

绑定代码若直接实现卷积，C++ 调用和 Python 调用会逐渐变成两套后端；测试若访问裸指针，又无法验证真实用户经过的接口。

## 构建扩展

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

Windows 的 Release 构建产物通常位于 `build/Release/mytensor.pyd`。`conftest.py` 在测试开始前把 `build/Release` 和 `build` 加入 `sys.path`，并用 `os.add_dll_directory()` 注册 CUDA 的 `bin` 目录。若 `.pyd` 文件明明存在却提示缺少模块，先检查依赖 DLL 和 Python ABI，别急着改绑定代码。

## 绑定层

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

激活函数作为 Tensor 方法，卷积、池化和全连接等多输入操作放在 `mytensor.nn`。这个选择不影响计算，却决定了接口以后是否容易扩展。Tensor 方法适合与单个对象紧密相关的操作，独立算子则更适合显式列出多个输入和参数。

绑定层还给 Tensor 定义了 `__repr__()`，只显示 shape 和 device，不把数据自动搬回 CPU。

```text
<Tensor shape=[2, 3] on GPU>
```

若 `repr` 顺手调用 `.numpy()`，在调试器或 Notebook 中查看变量也会触发同步和 D2H copy。元数据可以随时打印，真实数据则由调用者明确请求。

## NumPy 桥接

`Tensor.from_numpy()` 接收 C-contiguous 的 `float32` 数组。`forcecast` 会把其他可转换类型或非连续 view 整理成所需布局。

```cpp
Tensor numpy2tensor(
    py::array_t<float,
        py::array::c_style | py::array::forcecast> array);
```

绑定函数读取 `ndim` 和 `shape`，创建对应 Tensor，再复制连续数据。`numpy()` 走相反方向：先创建由 NumPy 管理的新数组，再把 CPU 或 GPU Tensor 的内容复制进去。

每一维先从 `py::ssize_t` 转成 `int`。源码在转换前检查是否超过 `int` 上限，避免大数组维度静默截断；Tensor 的底层 shape 仍然使用 `int`，因此这个限制属于公开接口的一部分。

`from_numpy()` 当前总是创建 GPU Tensor。即使传入的是普通 NumPy 数组，返回对象也已经完成 H2D copy；若机器没有可用 CUDA，转换阶段便会失败。这种约定让后面的算子入口简单，却也意味着 `from_numpy()` 不是一个纯粹的数据包装函数。

这里采用双向复制，没有共享存储。多占一份内存，却把生命周期变得很清楚。Python 数组释放后，Tensor 不会悬空；Tensor 析构后，已经返回的 NumPy 数组仍然有效。零拷贝需要同时处理 capsule、引用计数、stride、设备地址和只读约束，在接口还没有稳定时很容易得不偿失。

数据拷贝的位置也应集中在桥接层。若每个算子各自调用 `.numpy()` 或 `from_numpy()`，一次网络前向会在 Host 和 Device 间来回搬运，后端再快也没有意义。

标签也经过同一个 `float32` Tensor 通道。Python 测试传入整数标签时，`forcecast` 会把它转换成 `float`，CUDA kernel 再把数值当作类别编号比较。这是当前后端接口的历史约定，并不理想；若之后增加整型 Tensor，应让标签保留整数 dtype，避免类别索引先变成浮点数。

## 算子包装

每个 wrapper 都要完成参数检查、对象转换、算子调用和返回值整理。

1. 解析 Python 参数并检查维数。
2. 根据输入和 stride、padding 等参数计算输出形状。
3. 分配输出 Tensor。
4. 把底层指针与标量参数交给 CUDA 实现。

例如卷积接口应先确认输入和权重都是四维、通道数一致、输出高宽为正，再启动 kernel。若形状检查留到设备端，错误往往表现为越界访问，Python 只能看到一次含义不明的 CUDA 失败。

当前 wrapper 主要直接读取固定位置的 shape，例如 `image.getShape()[3]`。合法输入能够正常工作，维度不足时却会先越界访问。若把它当作真正可复用的 Python 包，shape 检查必须放在读取下标之前，并通过 `py::value_error` 抛出能看懂的异常。

反向接口还要统一返回顺序。全连接和卷积都返回输入、权重、偏置三类梯度；测试和后续自动微分层便可以按照固定契约接收，不需要了解底层如何计算。

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

返回顺序一旦约定，后续自动微分算子会依赖它；把 `dw` 与 `db` 调换不会在绑定层报错，只会把错误 shape 一路传到计算图中。

| 模块 | Python 输入 | 返回值 |
| --- | --- | --- |
| 激活函数 | 输入、上游梯度 | 输出或输入梯度 |
| 全连接 | 输入、权重、偏置 | 输出或三类梯度 |
| 卷积 | 输入、权重、偏置、步长与填充 | 输出或三类梯度 |
| 最大池化 | 输入、核大小与步长 | 输出或输入梯度 |
| 分类损失 | logits、标签 | 概率、损失或 logits 梯度 |

## 数据模块

`data/mnist.py` 只验证数据能经过 NumPy 进入自定义 Tensor，没有在本 Lab 训练网络。

```python
images = dataset.data.numpy().astype(np.float32) / 255.0
images = images[:, None, :, :]
tensor = mytensor.Tensor.from_numpy(images)
```

实际脚本逐个迭代 Dataset，因此 `ToImage`、转为 `float32` 和归一化都会执行，再由 `np.array` 拼成 batch。这样能验证 transform 的真实结果，但对完整 MNIST 会产生较多 Python 循环开销。若只需要原始像素，可以直接读取 `dataset.data`；若需要 transform，则更适合交给 DataLoader 分批处理。

## 测试分层

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

两类测试缺一不可。只对拍普通随机输入，边界分支可能从未执行；只测内部细节，又可能漏掉绑定层的类型和生命周期错误。

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

## 排查导入与数值错误

- 构建扩展和运行测试必须使用兼容的 Python ABI。`import mytensor` 失败时，应先核对 CMake 找到的解释器，而不是立刻怀疑 kernel。
- `forcecast` 提供了便利，也可能悄悄复制大数组。性能测试时要区分算子耗时和输入整理耗时。
- Python 异常应在启动 kernel 前抛出。设备端越界通常更难回溯到原始参数。
- 返回 NumPy 数组时必须明确谁拥有内存。局部 C++ 缓冲区不能直接作为无所有者的 Python view 返回。
- CUDA 错误可能在后续 `.numpy()` 才因同步而出现。调试时要在绑定边界检查 launch error，避免把错误归到回传函数。

导入失败与数值失败应分开处理。前者只检查 `.pyd` 路径、Python 版本和依赖 DLL；能够 `import mytensor` 后，再用一个 $2\times3$ Tensor 检查 NumPy 往返；最后才运行算子测试。若直接用完整 `pytest` 反复构建，错误信息很容易被大量测试输出淹没。

## 复验

```powershell
cmake -S src -B build
cmake --build build --config Release

$env:PYTHONPATH = "$(Resolve-Path build/Release)"
python -m pytest -q test
```

当前 13 项测试全部通过。

![](assets/labs/lab-04/pytest.png)

这 13 项测试覆盖了激活函数、全连接、卷积、池化、Softmax 与交叉熵的前后向。新增算子仍保留一份 PyTorch 对照，依次检查 binding 返回 shape、前向数值和反向数值，三项都通过后再接入计算图。
