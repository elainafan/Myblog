---
title: 从零开始的 CUDA 神经网络算子
date: 2025-11-12
categories:
    - AI
slug: ai-programming-lab-03
hidden: true
seriesOrder: 23
---

# 从零开始的 CUDA 神经网络算子

> [!CAUTION]
>
> **本笔记仅供参考，请勿抄袭。**

## 任务

Lab 3 要实现卷积网络里常用的五组核心计算：全连接、二维卷积、最大池化、Softmax，以及交叉熵。除了 Softmax 不单独写反向，其余模块都要给出正反向传播，并在 `main.cu` 中构造实例检查结果。

全连接和卷积的主体由单精度 cuBLAS 矩阵乘完成，参数使用 cuRAND 初始化。卷积采用 `im2col` 与 `col2im`，没有实现 depthwise、dilated、transposed convolution 和 unpooling。

## 文件结构

```text
Lab3/
├── main.cu
├── tensor.cu
├── tensor.h
└── tensor_kernel.h
```

`tensor_kernel.h` 保存五类算子的 kernel 与调用封装。`main.cu` 为每一类计算准备固定随机种子、形状和输出打印，因此同一份程序重复运行时结果不会变化。

编译环境为 CUDA Toolkit 12.4、MSVC 19.44、cuBLAS 与 cuRAND。

## 行主序与 cuBLAS

C++ 数组按行主序保存，而 cuBLAS 默认把矩阵解释为列主序。如果直接把行主序的 $A$ 、 $B$ 传给 `cublasSgemm`，矩阵尺寸和转置标志都会错位。

当前代码用 `sgem()` 包了一层适配：先按照行主序接口接收 $m$ 、 $n$ 、 $k$ 和转置标志，再转换为 cuBLAS 所需的调用顺序。这样上层仍可按通常的 $C=AB$ 阅读代码。

![BLAS 的三个层次](assets/slides/06-blas-levels.png)

`cublasSgemm` 属于 BLAS Level 3，计算形式为 $C\leftarrow\alpha AB+\beta C$ 。全连接前向、输入梯度和权重梯度都能落到 GEMM；卷积经过 `im2col` 后也会得到同一种接口。偏置广播和偏置梯度属于向量操作，仍由单独的 kernel 或归约完成。

这层封装还分配了临时矩阵并做转置，读起来直观，代价是额外的显存与转置开销。继续优化时可以利用

$$
(AB)^\mathsf{T}=B^\mathsf{T}A^\mathsf{T}
$$

交换操作数与维度，避免显式转置和额外显存。

## 全连接层

输入、权重与偏置分别记为

$$
X\in\mathbb{R}^{N\times C_{\mathrm{in}}},\qquad
W\in\mathbb{R}^{C_{\mathrm{out}}\times C_{\mathrm{in}}},\qquad
b\in\mathbb{R}^{C_{\mathrm{out}}}
$$

前向计算为

$$
Y=XW^\mathsf{T}+b
$$

偏置通过长度为 $N$ 的全一向量广播到整个 batch。反向传播分别为

$$
\mathrm{d}X=\mathrm{d}Y W
$$

$$
\mathrm{d}W=\mathrm{d}Y^\mathsf{T}X
$$

$$
\mathrm{d}b=\sum_{n=1}^{N}\mathrm{d}Y_n
$$

三条式子都能写成矩阵乘。实现时最容易混淆的是 `input_size` 与 `output_size`，建议先把每个矩阵的形状写在纸上，再决定 `CUBLAS_OP_N` 或 `CUBLAS_OP_T`。

## 二维卷积

### 输出形状

输入形状为 $N\times C\times H\times W$ ，卷积核形状为 $K\times C\times K_H\times K_W$ 。给定 padding 与 stride 后，输出空间尺寸为

$$
H_{\mathrm{out}}=\left\lfloor
\frac{H+2P_H-K_H}{S_H}
\right\rfloor+1
$$

$$
W_{\mathrm{out}}=\left\lfloor
\frac{W+2P_W-K_W}{S_W}
\right\rfloor+1
$$

作业示例使用 stride 1 与保持尺寸的 zero padding，代码本身仍允许传入其他卷积核、padding 和 stride。

### im2col

直接让一个 kernel 同时处理卷积窗口、通道和输出位置并不利于复用矩阵乘法。`im2col` 把每个输出位置看到的感受野展开成一列，得到

$$
X_{\mathrm{col}}\in
\mathbb{R}^{(CK_HK_W)\times(H_{\mathrm{out}}W_{\mathrm{out}})}
$$

越过输入边界的位置填零。卷积核展平为

$$
W_{\mathrm{row}}\in
\mathbb{R}^{K\times(CK_HK_W)}
$$

单张图像的卷积便化为

$$
Y_{\mathrm{col}}=W_{\mathrm{row}}X_{\mathrm{col}}+b
$$

![Im2col 的数据布局](assets/slides/07-im2col-layout.png)

截图把每个感受野排成特征矩阵的一行，当前代码则把它排成 $X_{\mathrm{col}}$ 的一列，两种表示只差一次转置。只要权重布局和 GEMM 参数与之配套，计算结果完全相同。

相邻窗口重叠的像素会在列矩阵中重复出现。这个布局用额外显存换来连续的 GEMM 输入，也把 padding 与 stride 的地址计算集中到了 `im2col` kernel 中，矩阵乘部分不再关心卷积窗口如何滑动。

kernel 由线性下标反推出输出位置、卷积核位置和输入通道，再计算对应的输入坐标。

```cpp
int h_in = h_out * stride_h - pad_h + k_h;
int w_in = w_out * stride_w - pad_w + k_w;

if (h_in >= 0 && h_in < H && w_in >= 0 && w_in < W) {
    output[index] = input[c * H * W + h_in * W + w_in];
} else {
    output[index] = 0.0f;
}
```

### col2im

反向传播中，权重梯度由输出梯度和 `im2col` 结果相乘得到。输入梯度先在列空间计算

$$
\mathrm{d}X_{\mathrm{col}}
=W_{\mathrm{row}}^\mathsf{T}\mathrm{d}Y_{\mathrm{col}}
$$

随后由 `col2im` 写回原输入。一个输入像素可能出现在多个重叠窗口中，因此这里必须累加所有窗口的贡献，不能简单地把列矩阵 reshape 回去。

权重和偏置由整个 batch 共享。每张图像计算出的 $\mathrm{d}W$ 与 $\mathrm{d}b$ 都要累加，而 $\mathrm{d}X$ 则写入该样本自己的区域。

## 最大池化

前向过程在每个池化窗口中寻找最大值。反向时只有最大值位置接收上游梯度，其余位置写零。

![Max Pooling 的反向传播](assets/slides/07-maxpool-backward.png)

```cpp
input_grad[index] += (value == max_value) ? grad_value : 0.0f;
```

图中的 mask 保存了每个窗口在前向时选中的 argmax，反向时只向这些位置散射梯度。当前测试使用不重叠窗口与连续随机输入，几乎不会出现并列最大值。如果窗口里有两个完全相同的最大值，代码按数值比较会把完整梯度同时写给两者，与只记录一个 argmax 的行为不同。要严格对齐 PyTorch，应在前向时保存最大值下标，反向时按下标散射梯度。

## Softmax 与交叉熵

Softmax 先减去每行最大值，再做指数与归一化

$$
p_{n,c}=
\frac{\exp(z_{n,c}-\max_j z_{n,j})}
{\sum_j\exp(z_{n,j}-\max_k z_{n,k})}
$$

减去最大值不会改变最终概率，却能避免较大的 logit 令指数溢出。实现使用 Thrust 在每一行上求最大值、指数和总和。

交叉熵对 batch 取平均

$$
L=-\frac{1}{N}\sum_{n=1}^{N}\log p_{n,y_n}
$$

Softmax 与交叉熵的反向合并后为

$$
\frac{\partial L}{\partial z_{n,c}}
=\frac{p_{n,c}-\mathbb{1}[c=y_n]}{N}
$$

合并后的式子不需要显式构造 Softmax 的雅可比矩阵，计算更短，数值也更稳定。

## 测试

| 模块 | 测试形状 | 检查内容 |
| --- | --- | --- |
| 全连接 | $2\times3$ 输入，输出维度 2 | 输出、输入梯度、权重梯度、偏置梯度 |
| 卷积 | $1\times1\times3\times4$ ， $3\times3$ 核 | 输出尺寸与三类梯度 |
| 最大池化 | $1\times4\times4$ ， $2\times2$ 核 | 窗口最大值和梯度落点 |
| Softmax | $2\times3$ logits | 每行概率和 |
| 交叉熵 | 两个样本、三个类别 | 标量损失和 logits 梯度 |

固定随机种子后，Softmax 两行概率和都为 1，交叉熵损失为 1.1317。合并反向梯度为

$$
\begin{bmatrix}
-0.3624 & 0.1831 & 0.1793\\
0.1636 & 0.1475 & -0.3111
\end{bmatrix}
$$

每行梯度之和为零，符合 Softmax 对 logits 整体平移不敏感的性质。卷积与全连接还要检查输出尺寸，池化则应确认每个窗口的梯度落在最大值位置。

这里的确定性实例适合排查维度和转置错误。更严格的数值对照放在 Lab 4 中完成，封装成 Python 扩展后，可以让每一项结果直接与 PyTorch 比较。

## 编译与运行

```bash
nvcc -std=c++17 --extended-lambda -Xcompiler=/utf-8 \
  main.cu tensor.cu -lcublas -lcurand -o build/lab3.exe
./build/lab3.exe
```

若链接阶段找不到 cuBLAS 或 cuRAND，先确认 CUDA Toolkit 的库目录已进入工具链。若数值正确但速度很慢，优先检查循环内的 `cudaMalloc`、显式转置和 `cudaDeviceSynchronize()`，这些开销通常比小尺寸 kernel 本身更显眼。
