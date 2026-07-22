---
title: 从零开始的优化器
date: 2025-12-04
categories:
    - AI
slug: ai-programming-lab-06
hidden: true
seriesOrder: 26
---

# 从零开始的优化器

> [!CAUTION]
>
> **本笔记仅供参考，请勿抄袭。**

## 任务

Lab 6 在 MNIST 上训练一个双层全连接分类器。需要完成数据读取、Softmax 交叉熵、网络梯度、mini-batch SGD 和 Adam，并比较训练集与测试集上的损失和错误率。

代码保留了 Lab 5 的自动微分文件，不过这次的训练入口直接用 NumPy 写出两层网络的前向与反向，优化器拿到的是明确的 $\mathrm{d}W_1$ 、 $\mathrm{d}W_2$ 。这样更容易把注意力放在参数更新与优化器状态上。

## 文件结构

```text
Lab6/
├── basic_operator.py
├── device.py
├── tensor.py
├── task0_operators.py
├── task0_autodiff.py
├── task1_optimizer.py
└── std_optimizer.py
```

`task1_optimizer.py` 是实际运行入口，包含 MNIST 读取、网络初始化、前向计算、损失、两种优化器和训练循环。`std_optimizer.py` 保留 PyTorch 优化器的参考实现，用于核对更新逻辑。

## 数据与网络

MNIST 训练集有 60000 张图像，测试集有 10000 张。每张 $28\times28$ 图像展平为 784 维向量，转换成 `float32` 后除以 255。

```python
X_tr = trainset.data.numpy().reshape(-1, 28 * 28)
X_te = testset.data.numpy().reshape(-1, 28 * 28)
X_tr = X_tr.astype(np.float32) / 255.0
X_te = X_te.astype(np.float32) / 255.0
```

代码虽然为 torchvision Dataset 传入了 `Normalize`，但随后直接读取 `dataset.data`，不会触发 transform。因此实际输入只缩放到 $[0,1]$ ，没有使用 MNIST 的均值和标准差做标准化。复现实验时以这条实际执行路径为准。

分类器没有偏置，结构为

$$
Z_1=XW_1
$$

$$
A_1=\max(Z_1,0)
$$

$$
Z_2=A_1W_2
$$

输入维度为 784，隐藏层宽度为 100，输出维度为 10。两种优化器都在随机种子 0 下重新初始化权重，保证它们从同一套参数出发。

## Softmax 交叉熵

先从每行 logits 中减去最大值，再计算概率

$$
P_{i,c}=
\frac{\exp(Z_{i,c}-\max_j Z_{i,j})}
{\sum_j\exp(Z_{i,j}-\max_k Z_{i,k})}
$$

平均交叉熵为

$$
L=-\frac{1}{N}\sum_{i=1}^{N}\log P_{i,y_i}
$$

代码用 log-sum-exp 形式直接计算损失，没有先得到概率再取对数。

```python
z_max = np.max(logits, axis=1, keepdims=True)
z_exp = np.exp(logits - z_max)
log_probs = (logits - z_max) - np.log(
    np.sum(z_exp, axis=1, keepdims=True)
)
loss = -log_probs[np.arange(logits.shape[0]), labels].mean()
```

对 logits 的梯度为

$$
\mathrm{d}Z_2=\frac{P-Y}{N}
$$

其中 $Y$ 是 one-hot 标签。其余梯度沿两次矩阵乘和 ReLU 继续传播

$$
\mathrm{d}W_2=A_1^\mathsf{T}\mathrm{d}Z_2
$$

$$
\mathrm{d}Z_1=(\mathrm{d}Z_2W_2^\mathsf{T})\odot\mathbb{1}[Z_1>0]
$$

$$
\mathrm{d}W_1=X^\mathsf{T}\mathrm{d}Z_1
$$

## SGD

训练集按 batch size 100 顺序切分，每个 batch 计算一次梯度并原地更新参数

$$
W\leftarrow W-\eta\,\mathrm{d}W
$$

本次使用的学习率为 0.2。`SGD_epoch()` 不返回新权重，而是直接修改传入列表中的数组。若在函数内部写成 `weights = new_weights`，只会替换局部变量，外层训练循环看不到更新。

当前代码没有在每个 epoch 前打乱样本。MNIST 原始训练集已经按某种顺序存储，顺序 mini-batch 会让优化轨迹受数据排列影响。若继续比较优化器，应先增加固定随机种子的 shuffle，再保证 SGD 与 Adam 使用同一批次顺序。

## Adam

Adam 为每个参数保存一阶矩、二阶矩和全局时间步

$$
m_t=\beta_1m_{t-1}+(1-\beta_1)g_t
$$

$$
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2
$$

初始时 $m_0$ 、 $v_0$ 都为零，前几个时间步会偏向零，因此还要做偏差修正

$$
\widehat m_t=\frac{m_t}{1-\beta_1^t}
$$

$$
\widehat v_t=\frac{v_t}{1-\beta_2^t}
$$

参数更新为

$$
W_t=W_{t-1}-
\eta\frac{\widehat m_t}{\sqrt{\widehat v_t}+\epsilon}
$$

实现使用 $\beta_1=0.9$ 、 $\beta_2=0.999$ 和 $\epsilon=10^{-8}$ 。最容易漏掉的是跨 epoch 保存状态。若每轮都重新创建 $m$ 、 $v$ 和 $t$ ，Adam 会反复回到第一步，历史动量全部丢失。

```python
state = {
    "m": [np.zeros_like(w) for w in weights],
    "v": [np.zeros_like(w) for w in weights],
    "t": 0,
}
```

`Adam_epoch()` 返回更新后的状态，训练循环再传给下一轮。

学习率仍然决定每次参数更新的尺度。步长过小时损失下降很慢，步长过大时会跨过低损失区域并发生震荡；Adam 的自适应分母只能改变各坐标的相对尺度，不能让任意大的基础学习率都稳定。

![学习率大小与收敛过程](assets/slides/12-learning-rate.png)

## 实验结果

两组实验都训练 20 个 epoch，batch size 为 100。SGD 学习率为 0.2，Adam 学习率为 0.02。

| 优化器 | 训练损失 | 训练错误率 | 测试损失 | 测试错误率 |
| --- | ---: | ---: | ---: | ---: |
| SGD | 0.02243 | 0.545% | 0.08322 | 2.440% |
| Adam | 0.12205 | 3.082% | 0.33932 | 5.020% |

SGD 的测试错误率从首轮的 5.85% 降到 2.44%。Adam 很快学到有效分类器，但随后损失和错误率有明显波动，最终结果不如 SGD。

这不能说明 Adam 天生弱于 SGD。0.02 对 Adam 来说偏大，而训练 batch 又没有打乱，两项因素都会放大更新震荡。更合理的后续实验是先把 Adam 学习率降到 $10^{-3}$ 附近，再固定数据顺序比较收敛速度。

## 运行

```bash
python task1_optimizer.py
```

程序依次训练 SGD 与 Adam，并在每个 epoch 后对完整训练集和测试集计算损失、错误率。测试集只用于报告结果，不参与参数更新。
