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

Lab 6 在 MNIST 上训练一个双层全连接网络，手写 Softmax 交叉熵、反向传播、mini-batch SGD 和 Adam。代码保留了 Lab 5 的自动微分模块，不过训练入口直接使用 NumPy 梯度，让优化器的状态和更新过程更容易观察。

训练程序可以拆成下面几块。

```text
parse_mnist()          数据入口
set_structure()       参数创建
forward()             模型计算
softmax_loss()        目标函数
SGD_epoch()/Adam_epoch()  参数更新
train_nn()            调度与评估
```

每个函数只处理一个阶段。优化器拿到参数和梯度，不负责读取数据；训练循环负责保存跨 epoch 状态，不重复实现更新公式。

## 数据与参数

`parse_mnist()` 把每张 $28\times28$ 图像展平为 784 维 `float32` 向量，缩放后的像素落在 $[0,1]$ 区间内。

```python
X_tr = trainset.data.numpy().reshape(-1, 28 * 28)
X_te = testset.data.numpy().reshape(-1, 28 * 28)
X_tr = X_tr.astype(np.float32) / 255.0
X_te = X_te.astype(np.float32) / 255.0
```

这里虽然给 torchvision Dataset 传入了 `Normalize`，后面却直接读取 `dataset.data`，因此 transform 不会执行。实际训练只做了除以 255。这个坑很隐蔽：代码中“写了标准化”不等于数据真的经过了标准化，必须沿真实的数据路径检查。

参数创建集中在 `set_structure()`。第一层权重 $W_1\in\mathbb{R}^{784\times h}$ 负责把图像映射到隐藏层，第二层权重 $W_2\in\mathbb{R}^{h\times10}$ 输出十类 logits。当前网络没有偏置。

```python
W1 = np.random.randn(n, hidden_dim).astype(np.float32) / np.sqrt(hidden_dim)
W2 = np.random.randn(hidden_dim, k).astype(np.float32) / np.sqrt(k)
return [W1, W2]
```

SGD 与 Adam 对比时要在相同随机种子下分别调用一次参数创建，不能让第二个优化器接着第一个已经训练过的权重继续跑。

## 前向与梯度

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

当前 `SGD_epoch()` 和 `Adam_epoch()` 内部各自写了一遍前向与反向。这样容易观察更新过程，却带来重复。更适合继续扩展的接口是单独提供 `backward(X, weights, y)`，返回与 `weights` 一一对应的梯度列表，两种优化器只消费这份列表。

## SGD 模块

`SGD_epoch()` 顺序切分 mini-batch，计算梯度后原地更新参数

$$
W\leftarrow W-\eta\,\mathrm{d}W
$$

```python
weights[0] -= lr * dW1
weights[1] -= lr * dW2
```

这里必须原地修改数组。若函数内部写成 `weights = new_weights`，只会替换局部列表，外层训练循环仍持有旧参数。使用 `weights[j] -= ...` 则保留对象身份，模型下一次前向能看到更新。

当前代码没有在 epoch 开始前打乱样本，batch 顺序会一直相同。若要比较优化器，应使用固定随机种子的 permutation，并让两种优化器读取相同批次；否则差异中还混入了数据顺序。

## Adam 模块

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

如果每个 epoch 都重新创建三个状态，其中 $m$ 保存一阶矩，变量 $v$ 保存二阶矩，变量 $t$ 保存步数，那么 Adam 会不断回到第一步，前面所有 batch 的历史都被清空。无状态 SGD 不必返回额外对象，有状态优化器则必须让状态跨越调用边界。

![学习率大小与收敛过程](assets/slides/12-learning-rate.png)

自适应分母并不能替代学习率。Adam 和 SGD 适合的基础步长通常不同，用同一数值直接比较并不公平。一次实验里 Adam 波动更大，应先检查学习率、batch 顺序和状态生命周期，再解释准确率差异。

## 训练调度

`train_nn()` 只做三件事：调用优化器跑完一轮、在完整训练集上评估、在测试集上评估。损失和错误率计算封装在 `loss_err()` 中，避免两份评估代码出现不同口径。

训练集与测试集的评估都只读取参数，不应修改 optimizer state。若以后把 Lab 5 的自动微分接回来，还需要在评估阶段关闭构图或及时释放图，否则每个 epoch 都会留下一整张无用计算图。

参数初始化也不应藏在 `train_nn()` 内部。调用者传入哪组权重，函数就训练哪组权重；否则外部设置的随机种子或预训练参数会被悄悄覆盖。

## 写的时候踩过的坑

- torchvision transform 被 `dataset.data` 绕过，实际预处理与代码表面不一致。
- 最后一个 batch 可能小于设定大小，归一化梯度时应使用当前 batch 的真实样本数。
- `weights` 与梯度列表必须保持相同顺序和形状，优化器不应靠变量名猜对应关系。
- Adam 的时间步按参数更新次数递增，不是按 epoch 递增。
- 一阶、二阶矩需要与参数同 dtype。默认创建 `float64` 状态会让内存和运算类型悄悄变化。
- 评估测试集只能用于观察泛化，不能据此反复挑选超参数；需要调参时应再划出验证集。

## 复验

```bash
python task1_optimizer.py
```

复验时关注训练损失能否下降、参数是否原地改变，以及 Adam 的 `t` 是否跨 epoch 连续增长。最终损失和错误率用于确认训练链路是否接通。
