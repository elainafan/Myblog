---
title: 卷积与池化
date: 2025-10-16
categories:
    - AI
slug: ai-programming-convolution-pooling
hidden: true
seriesOrder: 7
---

## 卷积

二维卷积让一个小窗口在输入上滑动。窗口每到一个位置，就把覆盖区域与卷积核逐元素相乘并求和，得到一个输出元素。

![局部连接与权重共享](assets/slides/07-local-connections.png)

对单通道输入，用 $W$ 表示 $3\times3$ 卷积核。当前窗口左上角坐标取 $(h,w)$ 时，输出为

$$
Y_{h,w} =
\sum_{i=0}^{2}
\sum_{j=0}^{2}
W_{i,j}X_{h+i,w+j}
$$

同一组 $W$ 会用于所有空间位置，这称为 weight sharing。全连接层要为每对输入、输出分别保存权重，卷积只连接局部窗口并复用参数，因此更适合图像。

输入平移后，输出特征也随之平移，这一性质称为 translation equivariance。它并不等于平移不变。只有继续做全局聚合、池化或其他丢弃位置信息的操作，最终表示才可能对小幅平移近似不变。

深度学习框架的 `conv2d` 实际执行 cross-correlation，不会把 kernel 先上下、左右翻转。网络训练会直接学到适合这一约定的权重，所以命名差异不影响使用。

### Batch 与 Channel

一批二维特征图的输入形状为 `[N, C_in, H, W]`。

- $N$ 是 batch size。
- $C_{\mathrm{in}}$ 是输入通道数。
- $H$ 与 $W$ 是空间高度和宽度。

权重形状为 `[C_out, C_in, K_H, K_W]`。一个输出通道拥有 $C_{\mathrm{in}}$ 个二维 kernel，它们分别处理各输入通道，最后沿通道求和。输出形状为 `[N, C_out, H_out, W_out]`。

用 $S$ 表示 stride，用 $D$ 表示 dilation，用 $P$ 表示 padding，输出元素为

$$
Y_{n,o,h,w} =
b_o
+
\sum_{c=0}^{C_{\mathrm{in}}-1}
\sum_{i=0}^{K_H-1}
\sum_{j=0}^{K_W-1}
W_{o,c,i,j}
X_{n,c,hS_H+iD_H-P_H,wS_W+jD_W-P_W}
$$

超出输入边界的位置按 padding 规则处理。输出高度为

$$
H_{\mathrm{out}} =
\left\lfloor
\frac{
H+2P_H-D_H(K_H-1)-1
}{
S_H
}
+1
\right\rfloor
$$

宽度同理。对于 $3\times3$ kernel，stride、padding 与 dilation 分别取 1、1、1 时，空间尺寸保持不变。

### 步幅与填充

Stride 决定窗口每次移动几格。Stride 为 $2$ 时，输出高宽大约减半，卷积同时完成特征提取与下采样。

Dilation 决定 kernel 相邻采样点之间的间隔。以 $3\times3$ kernel 为例，dilation 取 2 时覆盖的有效范围是 $5\times5$ 大小，参数数量仍为九个。

Padding 为边界附近的窗口提供输入。常见方案包括

- `constant` 使用常数填充，卷积中通常补零；
- `reflect` 从边界向内反射；
- `replicate` 复制边缘像素；
- `circular` 从另一侧循环取值。

边界规则会改变图像边缘的响应。训练与推理应使用同一种规则。

PyTorch 接口为

```python
torch.nn.functional.conv2d(
    input,
    weight,
    bias=None,
    stride=1,
    padding=0,
    dilation=1,
    groups=1,
)
```

## 卷积的矩阵化

朴素卷积包含 batch、输出通道、输入通道、输出坐标与 kernel 坐标等多层循环。直接写 CUDA kernel 可以完成计算，但成熟 GEMM 已经对缓存、shared memory、向量指令和 Tensor Core 做了大量优化。许多卷积实现会先改变数据布局，再调用矩阵乘法。

### 稀疏矩阵表示

将输入与输出全部展平后，卷积可以写成线性变换。矩阵的一行记录某个输出位置需要读取哪些输入元素，其余位置为零。

![卷积的稀疏矩阵表示](assets/imported/962042a8-0a64-4b27-b097-0e1c6dbaa788.png)

这张稀疏矩阵不对应一份新的可训练参数。卷积核中的同一个系数会出现在许多行中，因为它要作用于所有合法的空间位置。矩阵中看似不同的非零元，可能都对应卷积核里的同一个坐标，这正是 weight sharing 在矩阵表示中的样子。

设展开后的算子为 $\widetilde{W}$ ，前向传播可以写成 $Y=\widetilde{W}X$ 。输入梯度使用转置算子 $\widetilde{W}^\mathsf{T}$ ，它会把所有覆盖同一输入像素的输出梯度累加回来。Padding、stride 与 dilation 改变的只是非零元落在矩阵中的位置。

权重梯度还多一步归并。所有引用同一个卷积核系数的矩阵位置都共享一份参数，因此这些位置产生的梯度必须按 kernel 坐标求和，不能把它们当成彼此独立的矩阵元素更新。并行实现可以让线程先产生局部贡献，再用 Reduce 或按 key 的 segmented reduction 完成累加。

这种表示适合推导前向和反向关系，却不适合直接构造。矩阵中绝大多数元素为零，即使改成稀疏格式，索引与间接访存也会吞掉卷积规则结构带来的好处。稠密卷积通常采用 direct kernel、implicit GEMM 或 im2col，而不会真的保存 $\widetilde{W}$ 。

### Im2col

Im2col 不展开权重矩阵，而是把输入中的每个滑动窗口复制为一列。

![Im2col 的数据布局](assets/slides/07-im2col-layout.png)

若卷积窗口展开后的长度为

$$
K=C_{\mathrm{in}}K_HK_W
$$

每张图片共有 $H_{\mathrm{out}}W_{\mathrm{out}}$ 个窗口。把 batch 一并展开后，得到形状为

$$
K\times
\left(
NH_{\mathrm{out}}W_{\mathrm{out}}
\right)
$$

这就是展开矩阵 $\widetilde{X}$ 的尺寸。权重展开后的尺寸为 $C_{\mathrm{out}}\times K$ 大小，前向传播变成

$$
Y=W\widetilde{X}
$$

原来七层循环的大部分索引工作被移到 im2col，数值计算交给 GEMM。

Im2col 会复制重叠窗口。Stride 为 $1$ 的 $3\times3$ 卷积中，一个内部像素可能出现在九个窗口里，因此 $\widetilde{X}$ 会远大于原输入。它实现简单、容易复用高性能 GEMM，代价是额外工作区和内存流量。cuDNN 会根据形状、dtype、workspace 限制与硬件选择 direct、implicit GEMM 或其他算法，不会固定使用显式 im2col。

### 前向与反向

前向计算为

$$
Y=W\widetilde{X}+b
$$

给定记作 $\partial L/\partial Y$ 的上游梯度，权重梯度为

$$
\frac{\partial L}{\partial W} =
\frac{\partial L}{\partial Y}
\widetilde{X}^{\mathsf T}
$$

展开后输入的梯度为

$$
\frac{\partial L}{\partial\widetilde{X}} =
W^{\mathsf T}
\frac{\partial L}{\partial Y}
$$

Col2im 再把 $\partial L/\partial\widetilde{X}$ 放回原输入布局。多个窗口会覆盖同一输入位置，这些贡献必须相加。GPU 可以使用 atomic add，也可以重新分配任务，让每个 thread gather 自己负责的输入梯度。

Bias 对同一输出通道的所有 batch 与空间位置共享，因此 bias 梯度沿 batch、高度和宽度三个维度做 Reduce。

## 卷积变体

### 分组卷积

`groups` 把输入、输出通道划分为互不连接的组。普通卷积使用 `groups=1`，每个输出通道读取全部输入通道。

当 `groups=C_in` 且 $C_{\mathrm{out}}$ 是 $C_{\mathrm{in}}$ 的整数倍时，每组只包含一个输入通道，这就是 depthwise convolution。若输入、输出通道数相同，权重形状可以看成 `[C_in, 1, K_H, K_W]`。

普通卷积的一个输出元素需要 $C_{\mathrm{in}}K_HK_W$ 次乘法，depthwise convolution 只需 $K_HK_W$ 次。

![Depthwise convolution 的线程映射](assets/imported/1.png)

Depthwise convolution 不混合不同通道，通常再接一个 $1\times1$ pointwise convolution。Pointwise convolution 负责通道组合，depthwise convolution 负责空间邻域，两者合称 depthwise separable convolution。

计算量减少后，算子可能从 compute-bound 变为 memory-bound。理论 FLOPs 很低并不保证实际延迟按同样比例下降，布局转换和 kernel launch 的占比会变大。

### 转置卷积

普通卷积展平后可以写成线性变换

$$
Y=WX
$$

其输入梯度为

$$
\frac{\partial L}{\partial X} =
W^\mathsf{T}
\frac{\partial L}{\partial Y}
$$

Transposed convolution 把 $W^\mathsf{T}$ 对应的数据流当作新的前向算子。Stride 大于 $1$ 时，一个输入元素会向更大的输出平面散射贡献，重叠位置需要累加。

它常用于上采样，但不能恢复普通卷积已经丢掉的信息。名称中的 transposed 指线性变换矩阵的转置，不表示它是卷积的逆运算。

## Pooling

Pooling 在每个通道内独立聚合局部窗口。Max Pooling 取最大值，Average Pooling 取平均值。最常见的池化窗口大小为 $2\times2$ 且 stride 取 2，会把高宽各缩小一半。

```python
torch.nn.functional.max_pool2d(
    input,
    kernel_size,
    stride=None,
    padding=0,
    dilation=1,
    ceil_mode=False,
    return_indices=False,
)
```

`stride` 默认等于 `kernel_size`。`ceil_mode=True` 允许窗口从最后一个有效位置开始，即使它不能完整落入输入。`return_indices=True` 会额外返回每个窗口最大元素的位置。

### 池化反向

前向时除最大值外，还要保存 argmax。反向传播把上游梯度送回 argmax 指向的输入，窗口中其他位置得到零。

![Max Pooling 的反向传播](assets/slides/07-maxpool-backward.png)

若窗口互相重叠，同一输入元素可能同时成为多个窗口的最大值，需要累加多份梯度。Max Unpooling 也使用这些索引把值放回较大的稀疏平面，但它无法补回被池化丢弃的非最大元素。

卷积与池化都属于 stencil。每个输出从规则邻域 gather 数据，邻域较大或窗口重叠较多时，可以用 shared memory tile 复用输入。

## 分类输出与损失

### Softmax

分类网络输出的 logits 没有范围限制。Softmax 将一行 logits 变为和为 1 的正数，其定义为

$$
p_i =
\frac{e^{z_i}}
{\sum_j e^{z_j}}
$$

指数函数很容易上溢。令行最大值为 $m=\max_j z_j$ 并利用 Softmax 的平移不变性，可以改写为

$$
p_i =
\frac{e^{z_i-m}}
{\sum_j e^{z_j-m}}
$$

减去最大值后，最大的指数为 1，其余指数也不超过 1。CUDA 上的一行 Softmax 包含 row max、指数变换、row sum 与归一化。短行可以由一个 warp 负责，长行需要 block 级或多阶段 Reduce。

Softmax 的 Jacobian 为

$$
\frac{\partial p_i}{\partial z_j} =
p_i(\delta_{ij}-p_j)
$$

![Softmax 梯度](assets/imported/3.png)

### Cross Entropy

对 one-hot 标签 $y$ 和预测分布 $p$ 计算交叉熵

$$
L=-\sum_i y_i\log p_i
$$

![Cross Entropy](assets/imported/4.png)

Softmax 与 Cross Entropy 联合求导后，关于 logits 的梯度化为

$$
\frac{\partial L}{\partial z_i}=p_i-y_i
$$

![Softmax 与 Cross Entropy 的联合梯度](assets/imported/5.png)

实际实现不会先保存概率再逐项取对数，而是直接使用 LogSoftmax 或 log-sum-exp 计算损失。这样既避免极小概率下溢，也少写入一个中间 Tensor。
