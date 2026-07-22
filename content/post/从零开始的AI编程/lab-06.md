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

## 优化器简要介绍

Lab 6 在 MNIST 上训练一个双层全连接网络，Softmax 交叉熵、反向传播、mini-batch SGD 和 Adam 都用 NumPy 手写。目录里保留了上一份 Lab 的自动微分代码，不过本次入口 `task1_optimizer.py` 没有调用它，梯度公式直接写在 epoch 函数里。

## 在动手之前

mini-batch 训练每次只用一部分样本估计完整梯度。batch 内的 loss 和梯度按真实样本数取平均，最后一个不足 `batch_size` 的 batch 也要使用自己的长度，不能继续除以固定值。

Softmax 计算指数前先减去每行最大 logits，分类概率不会因此改变，却能避免较大正数让 `exp()` 溢出。交叉熵使用类别下标构造 one-hot 标签，logits 梯度为预测概率减去标签，再除以 batch 大小。

SGD 只使用当前梯度，更新函数可以没有额外状态。Adam 为每个参数保存一阶矩、二阶矩，并用全局步数做偏差修正；这三组状态必须跨 batch 和 epoch 延续。每轮重新创建状态会让 Adam 一直停在第一个时间步。

参数与梯度都用列表传递，并保持相同顺序。`SGD_epoch()` 和 `Adam_epoch()` 负责更新，`train_nn()` 负责切 batch、调用评估并打印指标。

## 开始动手！

```text
Lab6/
├── task1_optimizer.py   本次实现与训练入口
├── std_optimizer.py     对照代码
├── task0_*.py           上一份自动微分框架
└── utils.py             Tensor 构造工具
```

这一版直接使用 NumPy 数组计算梯度，Adam 的 $m$ 、 $v$ 和 $t$ 都保存在普通 Python 对象中。

训练入口依次调用下面几个函数。

```text
parse_mnist()          数据入口
set_structure()       参数创建
forward()             模型计算
softmax_loss()        目标函数
SGD_epoch()/Adam_epoch()  参数更新
train_nn()            调度与评估
```

`SGD_epoch()` 与 `Adam_epoch()` 目前各自包含一份完整的前向和反向，图中的 `forward()` 只用于整轮评估。修改网络结构时，三处前向和两处反向都要同步改动。

### MNIST 与参数初始化

`parse_mnist()` 把每张 $28\times28$ 图像展平为 784 维 `float32` 向量，缩放后的像素落在 $[0,1]$ 区间内。

```python
X_tr = trainset.data.numpy().reshape(-1, 28 * 28)
X_te = testset.data.numpy().reshape(-1, 28 * 28)
X_tr = X_tr.astype(np.float32) / 255.0
X_te = X_te.astype(np.float32) / 255.0
```

torchvision Dataset 虽然传入了 `Normalize`，后面读取的却是 `dataset.data`，transform 实际没有执行。进入训练的数据只做了除以 255，这一点要沿着 `parse_mnist()` 的真实读取路径确认。

MNIST 的四个数组最终 shape 为

| 数组 | shape | dtype |
| --- | --- | --- |
| `X_tr` | $60000\times784$ | `float32` |
| `y_tr` | $60000$ | 整型 |
| `X_te` | $10000\times784$ | `float32` |
| `y_te` | $10000$ | 整型 |

网络没有卷积层，展平不会破坏后续接口。改用 transform 中的标准化时，要删除手工除以 255，避免一份图像被缩放两次。

参数创建集中在 `set_structure()`。第一层权重 $W_1\in\mathbb{R}^{784\times h}$ 负责把图像映射到隐藏层，第二层权重 $W_2\in\mathbb{R}^{h\times10}$ 输出十类 logits。当前网络没有偏置。

```python
W1 = np.random.randn(n, hidden_dim).astype(np.float32) / np.sqrt(hidden_dim)
W2 = np.random.randn(hidden_dim, k).astype(np.float32) / np.sqrt(k)
return [W1, W2]
```

SGD 与 Adam 对比时要在相同随机种子下分别调用一次参数创建，不能让第二个优化器接着第一个已经训练过的权重继续跑。

当前代码分别用 $\sqrt{h}$ 和 $\sqrt{k}$ 缩放两层权重，而 fan-in 初始化通常使用输入维数 $784$ 和 $h$ 。实验保留源码的初始化，SGD 与 Adam 也从同一组随机数开始。

### 前向和反向

`forward()` 只完成两次矩阵乘和一次 ReLU

$$
Z_1=XW_1
$$

$$
A_1=\max(Z_1,0)
$$

$$
Z_2=A_1W_2
$$

损失使用稳定的 log-sum-exp 写法，先减去每行最大值。

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

其余梯度按模型模块的相反顺序传回

$$
\mathrm{d}W_2=A_1^\mathsf{T}\mathrm{d}Z_2
$$

$$
\mathrm{d}Z_1=(\mathrm{d}Z_2W_2^\mathsf{T})\odot\mathbb{1}[Z_1>0]
$$

$$
\mathrm{d}W_1=X^\mathsf{T}\mathrm{d}Z_1
$$

`SGD_epoch()` 和 `Adam_epoch()` 各自写了一遍前向与反向。两段代码都依次保存 $Z_1$ 、 $A_1$ 、 $Z_2$ ，再计算 `dW2` 和 `dW1`；两种优化器的差别只出现在参数更新处。修改网络结构时，这两段公式必须一起改。

源码中的 one-hot 数组没有显式指定 dtype，NumPy 会创建 `float64` 数组。较稳妥的写法是沿用 `probs.dtype`。

```python
y_one_hot = np.zeros(
    (batch_size, num_classes),
    dtype=probs.dtype,
)
```

若使用默认的 `float64`，`probs - y_one_hot` 会把整条梯度提升为 `float64`，随后原地写回 `float32` 权重时可能触发 casting 错误，或者让中间数组占用双倍内存。

### SGD

`SGD_epoch()` 顺序切分 mini-batch，计算梯度后原地更新参数

$$
W\leftarrow W-\eta\,\mathrm{d}W
$$

```python
weights[0] -= lr * dW1
weights[1] -= lr * dW2
```

这里必须原地修改数组。若函数内部写成 `weights = new_weights`，只会替换局部列表，外层训练循环仍持有旧参数。使用 `weights[j] -= ...` 则保留对象身份，模型下一次前向能看到更新。

最后一个 batch 不一定等于配置的 `batch`。循环用 `end_idx = min(start_idx + batch, num_examples)` 截断，梯度除数必须取 `X_batch.shape[0]`，不能始终除以 100。MNIST 的 60000 恰好整除 100，这个错误在默认参数下不会出现，换一个 batch size 才会暴露。

当前代码没有在 epoch 开始前打乱样本，batch 顺序始终相同。SGD 与 Adam 读取相同顺序，因此表中的差异仍然来自优化器与各自的学习率。

### Adam

Adam 除参数外还拥有一阶矩、二阶矩和全局步数

$$
m_t=\beta_1m_{t-1}+(1-\beta_1)g_t
$$

$$
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2
$$

$$
\widehat m_t=\frac{m_t}{1-\beta_1^t},\qquad
\widehat v_t=\frac{v_t}{1-\beta_2^t}
$$

$$
W_t=W_{t-1}-
\eta\frac{\widehat m_t}{\sqrt{\widehat v_t}+\epsilon}
$$

状态用一个字典保存，与参数列表保持相同结构。

```python
state = {
    "m": [np.zeros_like(w) for w in weights],
    "v": [np.zeros_like(w) for w in weights],
    "t": 0,
}
```

`Adam_epoch()` 接收上一轮状态并返回更新后的状态；`train_nn()` 在整个训练过程中持有它。

```python
adam_state = None

for epoch in range(epochs):
    adam_state = opti_epoch(
        X_tr,
        y_tr,
        weights,
        using_adam=True,
        adam_state=adam_state,
    )
```

如果每个 epoch 都重新创建状态，Adam 会不断回到第一步，前面所有 batch 的历史都被清空。`m`、`v` 和 `t` 因此由 `train_nn()` 保存，并在下一轮继续传入。

时间步在每个 mini-batch 开始时加一，不是在每个 epoch 加一。一个 epoch 有 600 次更新，第二轮第一个 batch 的 $t$ 应为 601。偏差修正中的指数依赖这个数，若把它当作 epoch 计数，前几轮的修正会偏得很明显。

状态列表与参数列表一一对应。

```text
weights = [W1, W2]
m       = [m1, m2]
v       = [v1, v2]
grads   = [dW1, dW2]
```

当前网络只有两组权重，并行列表足以保存参数、梯度和 Adam 状态；四个列表的第 $j$ 项始终对应同一个参数。

![学习率大小与收敛过程](assets/slides/12-learning-rate.png)

自适应分母并不能替代学习率。Adam 和 SGD 适合的基础步长通常不同，用同一数值直接比较并不公平。一次实验里 Adam 波动更大，应先检查学习率、batch 顺序和状态生命周期，再解释准确率差异。

### 训练与调试

`train_nn()` 每轮调用一次优化器，然后分别在完整训练集和测试集上评估。损失和错误率都由 `loss_err()` 计算，两处统计使用同一套公式。

入口为 SGD 和 Adam 各调用一次 `np.random.seed(0)`，因此二者拿到相同初始权重；学习率分别是 0.2 与 0.02。每轮打印训练、测试 loss 和错误率，训练结果不会反过来改变优化器选择。

训练集与测试集的评估只读取参数，不修改 optimizer state。每轮都在 60000 张训练图和 10000 张测试图上重新计算 loss 与错误率，打印口径与最终表格一致。

`softmax_loss()`、`SGD_epoch()` 和 `Adam_epoch()` 各写了一遍稳定 Softmax。只修其中一份，训练 loss 与评估 loss 就可能使用不同公式，因此修改时要同时核对三处。

### 成品代码

训练入口与两种优化器集中在 `task1_optimizer.py`，`std_optimizer.py` 保留对照实现，其余 `task0_*` 文件来自上一份自动微分框架，本次没有接入训练。`train_nn()` 负责逐轮调用 optimizer、评估并打印结果，SGD 与 Adam 的 batch 前向和反向分别写在各自函数中。完整代码见 [Lab 6 源码](https://github.com/elainafan/Programming-in-AI-2025Fall-PKU/tree/main/Lab6)。

### 实验结果

```bash
python task1_optimizer.py
```

20 个 epoch 后的结果为：

| 优化器 | 训练 loss | 训练错误率 | 测试 loss | 测试错误率 |
| --- | ---: | ---: | ---: | ---: |
| SGD | 0.02243 | 0.545% | 0.08322 | 2.440% |
| Adam | 0.12205 | 3.082% | 0.33932 | 5.020% |

当前 Adam 的学习率为 0.02，batch 顺序没有打乱，后半程出现明显震荡；表中结果只对应这组参数。
