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

Lab 3 要在上一份 Tensor 上补全连接、二维卷积、最大池化、Softmax 和交叉熵。逐元素 kernel 已经不够用了：全连接与卷积需要矩阵乘，卷积还要处理窗口展开，池化反向会遇到重复写入，Softmax 则要防止指数溢出。

```text
Lab3/
├── tensor.h           Tensor 与 CUDA 工具声明
├── tensor.cu          上一份 Lab 的基础算子
├── tensor_kernel.h    本次新增的神经网络算子
└── main.cu            五组独立的小规模测试
```

全连接、卷积、池化、Softmax 和交叉熵分别验收。每组测试独立分配输入与梯度，某个算子失败时不会牵连其他模块。

```text
Tensor 接口与形状检查
        ↓
算子封装：分配输出、组织临时量、调用前后向过程
        ↓
CUDA kernel、cuBLAS、cuRAND
```

`tensor.cu` 保留存储与基础 Tensor 行为，新增实现集中在 `tensor_kernel.h`。算子接口拿到的是裸指针和 shape 参数，输出空间仍由调用端准备。

## 公共后端

卷积和全连接看起来不同，展开后都依赖矩阵乘。代码用一层 `sgem()` 包装 `cublasSgemm`，上层继续按照行主序的 $C=AB$ 传入形状和转置标志，适配层再转换成 cuBLAS 的列主序参数。

![BLAS 的三个层次](assets/slides/06-blas-levels.png)

`cublasSgemm` 属于 BLAS Level 3，完成

$$
C\leftarrow\alpha AB+\beta C
$$

全连接前向、输入梯度和权重梯度都能调用它；卷积先经过 `im2col`，随后也落到同一个接口。偏置广播、偏置归约和数据重排仍由小型 CUDA kernel 完成。

`sgem()` 接收的 `m`、`n`、`k` 描述逻辑上的行主序矩阵，内部用两次 `cublasSgeam` 转置结果，并调整 `cublasSgemm` 的转置标志。调用处因而可以继续写熟悉的 $C=AB$ ，代价是每次矩阵乘都会申请一块 $m\times n$ 的临时显存。

布局错误通常比乘法公式更难查。C++ 数组按行主序保存，cuBLAS 默认按列主序解释。只要一个维度或转置标志写反，输出仍可能是一块形状正确的内存，却没有任何数值意义。调试时先写出每个操作数的逻辑形状，再对照 `m`、`n`、`k`，比直接改 `CUBLAS_OP_T` 靠谱得多。

当前适配层会创建临时矩阵并做显式转置，接口清楚，但多了一次分配和数据移动。源码中的 `temp` 还需要在返回前 `cudaFree()`；否则每调用一次 GEMM 就泄漏一块结果大小的显存。若直接按列主序重新解释数据，可以利用

$$
(AB)^\mathsf{T}=B^\mathsf{T}A^\mathsf{T}
$$

交换操作数和维度，让 cuBLAS 直接读取已有布局。

`cublasHandle_t` 也属于有状态资源。当前每次全连接、卷积都会 `cublasCreate()`，结束后再销毁，便于保持函数独立，却把初始化开销带进了每个 batch。训练框架中更合适的做法是由后端上下文持有一个 handle，并为它设置当前 stream。

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

源码中的四次关键调用可以直接按 shape 对照。

| 结果 | 左矩阵 | 右矩阵 | shape |
| --- | --- | --- | --- |
| $Y$ | $X$ | $W^\mathsf{T}$ | $N\times C_{\mathrm{out}}$ |
| $\mathrm{d}X$ | $\mathrm{d}Y$ | $W$ | $N\times C_{\mathrm{in}}$ |
| $\mathrm{d}W$ | $\mathrm{d}Y^\mathsf{T}$ | $X$ | $C_{\mathrm{out}}\times C_{\mathrm{in}}$ |
| $\mathrm{d}b$ | $\mathrm{d}Y^\mathsf{T}$ | $\mathbf{1}$ | $C_{\mathrm{out}}\times1$ |

偏置前向与反向都借助全一向量完成。前向用 $\mathbf{1}b^\mathsf{T}$ 广播，反向用 $\mathrm{d}Y^\mathsf{T}\mathbf{1}$ 沿 batch 求和。这样不必再写两个形状相近的小 kernel。

## 卷积

卷积模块由形状计算、`im2col`、GEMM、偏置和 `col2im` 组成。输入采用 NCHW 布局，卷积核依次保存输出通道、输入通道、高和宽。输出尺寸先由接口层算出

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

线性下标的拆解顺序必须和列矩阵布局完全一致。源码依次取出 `w_out`、`h_out`、`k_w`、`k_h`、`c`，因此最后两维是连续的输出位置。若只交换 `k_w` 与 `h_out` 的顺序，矩阵大小仍然正确，GEMM 也会正常返回，但每列已经不再是一块真实的感受野。

### 写回梯度

输入梯度先在列空间计算

$$
\mathrm{d}X_{\mathrm{col}}
=W_{\mathrm{row}}^\mathsf{T}\mathrm{d}Y_{\mathrm{col}}
$$

`col2im` 再把各列写回输入布局。一个像素可能被多个卷积窗口覆盖，所以写回必须累加，不能把列矩阵直接 reshape。这里没有让每个列元素去 `atomicAdd` 输入，而是让一个线程负责一个输入元素，在该线程内部枚举所有能覆盖它的窗口。写入地址互不冲突，代价是每个线程要做两层卷积核循环。

```cpp
if (h_out % stride_h == 0 && w_out % stride_w == 0) {
    h_out /= stride_h;
    w_out /= stride_w;

    if (0 <= h_out && h_out < out_h &&
        0 <= w_out && w_out < out_w) {
        val += col_grad[col_index];
    }
}
```

整除检查不能省略。只有与 stride 网格对齐的窗口才真正出现过；若直接做整数除法，未对齐的位置也会被错误地归到附近窗口。

权重和偏置由整个 batch 共用。源码按样本循环，每张图像都重新做一次 `im2col`。计算 $\mathrm{d}W$ 和 $\mathrm{d}b$ 时，`sgem()` 的 `beta` 取 1，把本张图的结果加到已有梯度；计算 $\mathrm{d}X_{\mathrm{col}}$ 时 `beta` 取 0，因为每个样本都有独立的输入梯度区域。

进入循环前必须把 `weight_grad` 和 `bias_grad` 清零，否则 `beta=1` 会把未初始化显存也加进去。只用 batch size 为 1 的测试很难发现累计错误，至少要补一个两张图的例子。

## 最大池化

池化前向寻找每个窗口的最大值，反向把上游梯度送回最大值位置。

![Max Pooling 的反向传播](assets/slides/07-maxpool-backward.png)

保存 argmax 比在反向时重新比较数值更可靠。当前实现按 `value == max_value` 判断；窗口出现多个相同最大值时，它会把完整梯度写给每个相等位置，而常见框架只把梯度送给前向记录的一个下标。随机输入不容易触发这个差异，专门构造含并列最大值的测试才能发现。

池化窗口重叠时，多个输出也可能把梯度送到同一输入位置。此处和 `col2im` 一样，需要累加而非覆盖。

当前 max-pool kernel 的索引只有 $C\times H_{\mathrm{out}}\times W_{\mathrm{out}}$ ，没有 batch 维，`main.cu` 也只测试单张输入。接进网络以前需要在 Host 端逐样本调用，或者把 $N$ 加进 kernel 下标。否则第一张图之后的数据根本不会被处理。

反向实现直接对 `input_grad[...] += grad_val`。当窗口互不重叠时没有冲突；stride 小于池化核时，不同线程可能同时写同一个输入位置，需要 `atomicAdd`，或者改成与 `col2im` 类似的一输入一线程写法。

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

这份实现的 Softmax 没有手写归约 kernel，而是对 batch 中每一行依次调用 Thrust：先 `reduce` 求最大值，再 `transform` 求指数，第二次 `reduce` 求和，最后归一化。代码很短，也自带数值稳定化；batch 较大时，每行四次独立调度会产生不少开销。后续可以把一行交给一个 block，在 shared memory 中完成两次归约。

交叉熵前向让每个样本线程计算自身损失，再用 `atomicAdd` 加到一个标量中。因此调用前必须把 `loss` 清零。若上一轮的 loss 留在显存里，本轮输出会在旧值上继续累加，单看曲线很像训练突然发散。

## 测试顺序

`main.cu` 为各模块设置了不同的固定随机种子。卷积、全连接和池化的上游梯度直接填 1，方便人工核对归约；Softmax 额外检查每行概率和；交叉熵使用明确的标签下标。

输出依次检查 shape、前向不变量、反向归约方向和边界输入。

1. 先核对 shape 和输入是否完整写入。
2. 再检查前向中的简单不变量，例如 Softmax 每行和为 1。
3. 把上游梯度设为全 1，观察反向的归约方向。
4. 最后换成非方形输入、不同 stride 和 padding，查高宽是否写反。

随机小数适合发现大面积错误，但不适合查边界。卷积还应单独放一个手算得出的 $1\times1\times3\times4$ 输入；池化则要构造并列最大值和重叠窗口。

## 实现中的坑

- cuBLAS、cuRAND handle 应集中创建和销毁。每个小算子临时创建 handle 会把管理开销带进热路径。
- 临时显存也要逐一释放。`im2col`、转置矩阵和全一向量一旦漏掉，就会随着 batch 数持续占用显存；当前 `sgem()` 的 `temp` 正好需要补上这一步。
- kernel launch 后立即同步便于调试，却让各算子无法并行。正确性稳定后，应把同步移到测试边界或真正需要读取结果的地方。
- 前向和反向必须采用完全相同的 padding、stride 与布局约定。单独看每段公式都正确，也可能因为约定不同而接不上。
- 输出形状要在分配前验证。负数或不能整除的空间尺寸不应留到 kernel 内变成越界访问。

这些问题通常不会让编译器报错。输出 shape 仍然正确，程序也能跑完，只是数值从某一层开始偏离，所以每个模块都要留下能独立运行的小测试。

## 复验

`main.cu` 为五类计算准备固定随机种子和小尺寸输入，分别检查前向、输入梯度、参数梯度与输出形状。Softmax 每行概率和应接近 1，合并后的 logits 梯度每行之和应接近 0。

```bash
nvcc -std=c++17 --extended-lambda -Xcompiler=/utf-8 \
  main.cu tensor.cu -lcublas -lcurand -o build/lab3.exe
./build/lab3.exe
```

确定性小样例适合排查矩阵布局和下标。若 Softmax 的行和不对，先停在 Softmax；若卷积前向已经错了，也不要急着看卷积反向。等这些 C++ 测试稳定后，再交给 Python 与 PyTorch 对拍，错误范围会小很多。
