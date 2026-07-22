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

前三次 Lab 的 CUDA Tensor 只能由 C++ 调用。Lab 4 用 pybind11 把它封装成 `mytensor`，让 Python 能创建 Tensor、与 NumPy 交换数据，并调用已经实现的神经网络算子。

新增公式很少，工作集中在建立一条稳定的跨语言调用链。

```text
Python / NumPy
      ↓ pybind11
Tensor 接口与形状检查
      ↓
CUDA 算子与显存
```

Python 只接触公开对象，绑定层负责类型、形状与所有权转换，底层 CUDA 代码不需要知道调用者来自 Python。

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

Python 端只需要按照下面的顺序使用。

```python
array = np.random.randn(2, 3).astype(np.float32)
tensor = mytensor.Tensor.from_numpy(array)
output = tensor.relu_forward()
result = output.numpy()
```

激活函数作为 Tensor 方法，卷积、池化和全连接等多输入操作放在 `mytensor.nn`。这个选择不影响计算，却决定了接口以后是否容易扩展。Tensor 方法适合与单个对象紧密相关的操作，独立算子则更适合显式列出多个输入和参数。

## NumPy 桥接

`Tensor.from_numpy()` 接收 C-contiguous 的 `float32` 数组。`forcecast` 会把其他可转换类型或非连续 view 整理成所需布局。

```cpp
Tensor numpy2tensor(
    py::array_t<float,
        py::array::c_style | py::array::forcecast> array);
```

绑定函数读取 `ndim` 和 `shape`，创建对应 Tensor，再复制连续数据。`numpy()` 走相反方向：先创建由 NumPy 管理的新数组，再把 CPU 或 GPU Tensor 的内容复制进去。

这里采用双向复制，没有共享存储。多占一份内存，却把生命周期变得很清楚。Python 数组释放后，Tensor 不会悬空；Tensor 析构后，已经返回的 NumPy 数组仍然有效。零拷贝需要同时处理 capsule、引用计数、stride、设备地址和只读约束，在接口还没有稳定时很容易得不偿失。

数据拷贝的位置也应集中在桥接层。若每个算子各自调用 `.numpy()` 或 `from_numpy()`，一次网络前向会在 Host 和 Device 间来回搬运，后端再快也没有意义。

## 算子包装

绑定层不只是改函数名。它还承担四件事。

1. 解析 Python 参数并检查维数。
2. 根据输入和 stride、padding 等参数计算输出形状。
3. 分配输出 Tensor。
4. 把底层指针与标量参数交给 CUDA 实现。

例如卷积接口应先确认输入和权重都是四维、通道数一致、输出高宽为正，再启动 kernel。若形状检查留到设备端，错误往往表现为越界访问，Python 只能看到一次含义不明的 CUDA 失败。

反向接口还要统一返回顺序。全连接和卷积都返回输入、权重、偏置三类梯度；测试和后续自动微分层便可以按照固定契约接收，不需要了解底层如何计算。

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

数据读取与后端保持解耦后，CUDA 扩展不必依赖 torchvision。以后更换数据集时，只改 Python 端的预处理和 shape，底层仍接收连续 Tensor。

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

## 接口边界的坑

- 构建扩展和运行测试必须使用兼容的 Python ABI。`import mytensor` 失败时，应先核对 CMake 找到的解释器，而不是立刻怀疑 kernel。
- `forcecast` 提供了便利，也可能悄悄复制大数组。性能测试时要区分算子耗时和输入整理耗时。
- Python 异常应在启动 kernel 前抛出。设备端越界通常更难回溯到原始参数。
- 返回 NumPy 数组时必须明确谁拥有内存。局部 C++ 缓冲区不能直接作为无所有者的 Python view 返回。
- CUDA 错误可能在后续 `.numpy()` 才因同步而出现。调试时要在绑定边界检查 launch error，避免把错误归到回传函数。

## 复验

```powershell
cmake -S src -B build
cmake --build build --config Release

$env:PYTHONPATH = "$(Resolve-Path build/Release)"
python -m pytest -q test
```

当前 13 项测试全部通过。

![](assets/labs/lab-04/pytest.png)

这张结果说明公开调用链可以正确工作。继续扩展框架时，新的算子仍沿用同一条路径：先在后端实现，再绑定接口，最后用 NumPy 或 PyTorch 对拍。Python 层不再另写一份后端实现。
