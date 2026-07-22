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

Lab 3 在上一份 Tensor 上补全连接、二维卷积、最大池化、Softmax 和交叉熵。公共工作拆成三层，各算子沿同一条调用链组合已有模块。

```text
Tensor 接口与形状检查
        ↓
算子封装：分配输出、组织临时量、调用前后向过程
        ↓
CUDA kernel、cuBLAS、cuRAND
```

`tensor.cu` 保留存储与基础 Tensor 行为，`tensor_kernel.h` 保存算子后端，`main.cu` 只构造确定性小样例。上层关注张量形状和调用顺序，底层关注指针、线程和矩阵乘参数。

## 公共后端

卷积和全连接看起来不同，展开后都依赖矩阵乘。代码用一层 `sgem()` 包装 `cublasSgemm`，上层继续按照行主序的 $C=AB$ 传入形状和转置标志，适配层再转换成 cuBLAS 的列主序参数。

![BLAS 的三个层次](assets/slides/06-blas-levels.png)

`cublasSgemm` 属于 BLAS Level 3，完成

$$
C\leftarrow\alpha AB+\beta C
$$

全连接前向、输入梯度和权重梯度都能调用它；卷积先经过 `im2col`，随后也落到同一个接口。偏置广播、偏置归约和数据重排仍由小型 CUDA kernel 完成。

布局错误通常比乘法公式更难查。C++ 数组按行主序保存，cuBLAS 默认按列主序解释。只要一个维度或转置标志写反，输出仍可能是一块形状正确的内存，却没有任何数值意义。调试时先写出每个操作数的逻辑形状，再对照 `m`、`n`、`k`，比直接改 `CUBLAS_OP_T` 靠谱得多。

当前适配层会创建临时矩阵并做显式转置，接口清楚，但多了一次分配和数据移动。后续可以利用

$$
(AB)^\mathsf{T}=B^\mathsf{T}A^\mathsf{T}
$$

交换操作数和维度，让 cuBLAS 直接读取已有布局。

## 全连接

输入、权重和偏置的形状为

$$
X\in\mathbb{R}^{N\times C_{\mathrm{in}}},\qquad
W\in\mathbb{R}^{C_{\mathrm{out}}\times C_{\mathrm{in}}},\qquad
b\in\mathbb{R}^{C_{\mathrm{out}}}
$$

前向模块先用 GEMM 计算主体，再用全一向量把偏置广播到 batch

$$
Y=XW^\mathsf{T}+b
$$

反向模块返回三个彼此独立的结果

$$
\mathrm{d}X=\mathrm{d}Y W
$$

$$
\mathrm{d}W=\mathrm{d}Y^\mathsf{T}X
$$

$$
\mathrm{d}b=\sum_{n=1}^{N}\mathrm{d}Y_n
$$

这个接口设计比在调用端分别求三类梯度更稳妥：输入、权重和偏置共享同一份形状信息，算子内部可以一次完成校验和临时资源准备。测试时则要分别检查三个返回值，不能只确认前向输出。

## 卷积

卷积模块由形状计算、`im2col`、GEMM、偏置和 `col2im` 组成。输入采用 NCHW 布局，卷积核依次保存输出通道、输入通道、高和宽。输出尺寸先由接口层算出

$$
H_{\mathrm{out}}=left\lfloor
\frac{H+2P_H-K_H}{S_H}
\right\rfloor+1
$$

$$
W_{\mathrm{out}}=left\lfloor
\frac{W+2P_W-K_W}{S_W}
\right\rfloor+1
$$

### 展开窗口

`im2col` 把每个输出位置对应的感受野展成一列

$$
X_{\mathrm{col}}\in
\mathbb{R}^{(CK_HK_W)\times(H_{\mathrm{out}}W_{\mathrm{out}})}
$$

卷积核展平为

$$
W_{\mathrm{row}}\in
\mathbb{R}^{K\times(CK_HK_W)}
$$

单张图像的前向便成为

$$
Y_{\mathrm{col}}=W_{\mathrm{row}}X_{\mathrm{col}}+b
$$

![Im2col 的数据布局](assets/slides/07-im2col-layout.png)

`im2col` kernel 由一个线性下标反推出通道、卷积核位置和输出坐标。落在 padding 区域的元素写零，其余位置从输入取值。

```cpp
int h_in = h_out * stride_h - pad_h + k_h;
int w_in = w_out * stride_w - pad_w + k_w;

if (h_in >= 0 && h_in < H && w_in >= 0 && w_in < W) {
    output[index] = input[c * H * W + h_in * W + w_in];
} else {
    output[index] = 0.0f;
}
```

这一步把复杂的窗口寻址集中在一个模块里。GEMM 不需要知道 stride 和 padding，卷积核也不需要自己处理边界。代价是重叠窗口会复制相同像素，临时矩阵可能远大于原输入。

### 写回梯度

输入梯度先在列空间计算

$$
\mathrm{d}X_{\mathrm{col}}
=W_{\mathrm{row}}^\mathsf{T}\mathrm{d}Y_{\mathrm{col}}
$$

`col2im` 再把各列写回输入布局。一个像素可能被多个卷积窗口覆盖，所以写回必须累加，不能把列矩阵直接 reshape。并行 kernel 若让多个线程同时写同一位置，还要使用原子加或换一种无冲突的线程映射。

权重和偏置由整个 batch 共用。每张图像都会得到两类参数梯度，其中 $\mathrm{d}W$ 对应权重，变量 $\mathrm{d}b$ 对应偏置，两者都要继续累加。输入梯度 $\mathrm{d}X$ 只写入该样本对应的区域。忘记前两项的 batch 累加时，小样例可能仍能通过，batch size 大于一才会暴露问题。

## 最大池化

池化前向寻找每个窗口的最大值，反向把上游梯度送回最大值位置。

![Max Pooling 的反向传播](assets/slides/07-maxpool-backward.png)

保存 argmax 比在反向时重新比较数值更可靠。当前实现按 `value == max_value` 判断；窗口出现多个相同最大值时，它会把完整梯度写给每个相等位置，而常见框架只把梯度送给前向记录的一个下标。随机输入不容易触发这个差异，专门构造含并列最大值的测试才能发现。

池化窗口重叠时，多个输出也可能把梯度送到同一输入位置。此处和 `col2im` 一样，需要累加而非覆盖。

## Softmax 与交叉熵

Softmax 先减去每行最大值，再计算指数和归一化

$$
p_{n,c}=
\frac{\exp(z_{n,c}-\max_j z_{n,j})}
{\sum_j\exp(z_{n,j}-\max_k z_{n,k})}
$$

交叉熵对 batch 取平均

$$
L=-\frac{1}{N}\sum_{n=1}^{N}\log p_{n,y_n}
$$

两者的反向合并后为

$$
\frac{\partial L}{\partial z_{n,c}}
=\frac{p_{n,c}-\mathbb{1}[c=y_n]}{N}
$$

合并接口省去了 Softmax 雅可比矩阵，也避免先得到极小概率再取对数。这里仍要统一标签表示：类别下标和 one-hot Tensor 对应不同的 kernel 输入，若 Python 层和 CUDA 层各自假设一种格式，很容易读错显存。

## 模块间的坑

- cuBLAS、cuRAND handle 应集中创建和销毁。每个小算子临时创建 handle 会把管理开销带进热路径。
- 临时显存也应有清楚的所有者。`im2col`、转置矩阵和全一向量一旦在异常路径漏掉，就会随着 batch 数持续占用显存。
- kernel launch 后立即同步便于调试，却让各算子无法并行。正确性稳定后，应把同步移到测试边界或真正需要读取结果的地方。
- 前向和反向必须采用完全相同的 padding、stride 与布局约定。单独看每段公式都正确，也可能因为约定不同而接不上。
- 输出形状要在分配前验证。负数或不能整除的空间尺寸不应留到 kernel 内变成越界访问。

这些错误往往发生在模块连接处，因此测试不能只验证单个 kernel。

## 复验

`main.cu` 为五类计算准备固定随机种子和小尺寸输入，分别检查前向、输入梯度、参数梯度与输出形状。Softmax 每行概率和应接近 1，合并后的 logits 梯度每行之和应接近 0。

```bash
nvcc -std=c++17 --extended-lambda -Xcompiler=/utf-8 \
  main.cu tensor.cu -lcublas -lcurand -o build/lab3.exe
./build/lab3.exe
```

确定性小样例适合排查矩阵布局和下标。下一份 Lab 会把这些接口绑定到 Python，再用 PyTorch 对拍随机输入；两种测试分别守住内部计算和公开接口。
