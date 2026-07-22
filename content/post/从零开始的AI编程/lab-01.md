---
title: 从零开始的 CIFAR-10 图像分类
date: 2025-09-24
categories:
    - AI
slug: ai-programming-lab-01
hidden: true
seriesOrder: 21
---

# 从零开始的 CIFAR-10 图像分类

> [!CAUTION]
>
> **本笔记仅供参考，请勿抄袭。**

## CIFAR-10 分类简要介绍

Lab 1 要用 PyTorch 完成 CIFAR-10 分类。提交内容只有一个 `test.py`，数据处理、LeNet、十轮训练、整体准确率、分类别准确率和 loss 曲线都写在其中，最后再比较 SGD 是否使用 momentum 时的差别。

## 在动手之前

分类网络接收一个 batch 的图像，输出每个类别对应的 logits。`nn.CrossEntropyLoss()` 内部已经包含 LogSoftmax 与负对数似然，模型末尾直接返回形状为 $N\times10$ 的 logits，标签则是形状为 $N$ 的类别下标。若在 `forward()` 末尾再手动做一次 Softmax，数值会被重复归一化。

卷积层的输出尺寸由输入尺寸、kernel、padding 和 stride 共同决定。CIFAR-10 的输入为 $32\times32$ ，LeNet 使用两次 $5\times5$ 卷积和两次 $2\times2$ 池化，空间尺寸依次变为 $32\to28\to14\to10\to5$ 。展平时必须保留第 0 维的 batch，否则不同样本会被拼进同一个向量。

PyTorch 的一次训练更新固定经过 `zero_grad()`、前向、计算 loss、`backward()` 和 `step()`。梯度默认累加，因此少一次 `zero_grad()` 就会把相邻 batch 的梯度混在一起。评估阶段使用 `eval()` 切换层状态，再用 `inference_mode()` 关闭自动微分；二者不能互相替代。

## 开始动手！

### 环境与入口

程序从 `main()` 开始，先选设备，再依次创建数据、模型、损失函数、优化器和 TensorBoard writer。

```python
def main():
    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    model = LeNet().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(
        model.parameters(),
        lr=0.01,
        momentum=0.9,
        weight_decay=1e-4,
    )
```

设备只在入口处决定。模型和每个 batch 都搬到同一个 `device`，`forward()` 内部不再出现 CPU、CUDA 分支。Windows 下 DataLoader 会以 `spawn` 创建子进程，所以入口还要放进保护语句。

```python
if __name__ == "__main__":
    main()
```

漏掉这层保护后，worker 会重新导入并执行整个文件，随后出现重复下载、重复打印，或者一直卡在创建 DataLoader 的位置。

### 数据处理

每张 CIFAR-10 图像包含三个通道，每个通道的高和宽都是 32。训练集使用随机水平翻转和带四像素填充的随机裁剪，测试集只做张量转换与归一化。

```python
transform_train = transforms.Compose(
    [
        transforms.RandomHorizontalFlip(),
        transforms.RandomCrop(32, padding=4),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ]
)

transform_test = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ]
)
```

训练和测试使用两套 transform。若测试集也带随机裁剪，每次评估看到的图像都会变化，准确率便失去了可比性。训练 loader 打乱样本，测试 loader 保持固定顺序，两边都返回 `(inputs, labels)`。

变换顺序不能随意交换。`RandomCrop` 和 `RandomHorizontalFlip` 处理图像，`ToTensor()` 才把像素缩放到 $[0,1]$ 并改成 CHW 布局；归一化放在最后，将每个通道变换为

$$
x'=\frac{x-0.5}{0.5}
$$

因此网络实际接收的数值大致落在 $[-1,1]$ 。测试集沿用同一组均值和标准差，只去掉随机增强。

```python
trainloader = DataLoader(
    trainset,
    batch_size=32,
    shuffle=True,
    num_workers=2,
)
testloader = DataLoader(
    testset,
    batch_size=32,
    shuffle=False,
    num_workers=2,
)
```

`shuffle=True` 只改变样本进入 batch 的顺序，不改变数据集内容。测试阶段关闭 shuffle 后，分类别统计和异常样本定位都更容易复现。

### LeNet

LeNet 由两组卷积、池化和三层全连接组成

$$
3\xrightarrow{5\times5\ \mathrm{Conv}}6
\xrightarrow{2\times2\ \mathrm{MaxPool}}6
\xrightarrow{5\times5\ \mathrm{Conv}}16
\xrightarrow{2\times2\ \mathrm{MaxPool}}16
$$

空间尺寸依次变化为

$$
32\to28\to14\to10\to5
$$

最后一组特征图共有 16 个通道，展平后得到 400 个特征。

先把 shape 顺着 `forward()` 写一遍，全连接层的输入维数就不容易算错。

| 位置 | shape |
| --- | --- |
| 输入 | $N\times3\times32\times32$ |
| `conv1` | $N\times6\times28\times28$ |
| `pool1` | $N\times6\times14\times14$ |
| `conv2` | $N\times16\times10\times10$ |
| `pool2` | $N\times16\times5\times5$ |
| `flatten` | $N\times400$ |
| 输出 | $N\times10$ |

`torch.flatten(x, 1)` 保留第 0 维的 batch，只把后面的通道和空间维合并。若直接写成 `x.flatten()`，整个 batch 会被压成一维，第一层全连接便无法区分样本。

```python
class LeNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)
```

![LeNet 的前向、损失与反向传播](assets/slides/01-lenet-training.png)

`forward()` 末尾不接 Softmax，直接把 logits 交给 `CrossEntropyLoss()`。这份 LeNet 一共有 62006 个可训练参数。

### 训练循环

一个 batch 的更新直接写成下面五行。

```python
optimizer.zero_grad()
outputs = model(inputs)
loss = criterion(outputs, labels)
loss.backward()
optimizer.step()
```

`zero_grad()` 必须发生在下一次反向传播前。PyTorch 默认累加梯度，漏掉这一步以后，当前 batch 会把前面所有 batch 的梯度一起用于更新。`backward()` 只填写各参数的 `.grad`，真正修改参数的是 `optimizer.step()`，两者也不能颠倒。

当前 LeNet 没有 Dropout 和 Batch Normalization，`model.train()` 与 `model.eval()` 不会改变数值；代码仍在训练和测试入口明确切换模式。

```python
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0

    for inputs, labels in trainloader:
        inputs = inputs.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
```

`loss.item()` 会把标量取回主机，适合每个 batch 记一次日志。若把整块 `loss` Tensor 存进 Python 列表，它仍可能保留计算图引用，长训练中会不断占用内存。

整轮训练只负责重复上述单步，并累计 `loss.item()`。epoch loss 应除以 batch 数；若只记录最后一个 batch，曲线会对样本顺序非常敏感。TensorBoard writer 和模型保存放在训练循环外侧，不让记录代码混进参数更新逻辑。

### Momentum 对比

普通 SGD 只看当前梯度。加入动量后，优化器还保存跨 batch 的速度项

$$
v_t=m v_{t-1}+g_t
$$

$$
\theta_t=\theta_{t-1}-\eta v_t
$$

连续几个 batch 的梯度方向接近时，历史项会加快这一方向的移动；梯度来回摆动时，它又能削弱单个 batch 带来的突变。重新创建 optimizer 会丢掉动量缓冲区，只保存模型参数也不足以无缝续训。

代码还设置了 `weight_decay=1e-4`。PyTorch 的 SGD 会把参数本身按这个系数加入更新，用来限制权重继续增大。比较 momentum 时，其余参数应保持一致，否则曲线同时混进学习率、正则化和初始化的变化。

比较动量时，网络初始化、数据顺序和随机增强都应使用相同随机种子。原实验只固定了网络结构与训练轮数，因此曲线能说明当次运行的差异，不能当成严格的统计结论。

### 分类准确率

评估前切换到 `eval()`，并使用 `torch.inference_mode()` 关闭计算图记录。

```python
model.eval()

with torch.inference_mode():
    for inputs, labels in testloader:
        outputs = model(inputs.to(device))
        predicted = outputs.argmax(dim=1)
```

整体准确率累计预测正确的样本数，分类别准确率则为每个标签分别维护 `correct` 和 `total`，避免整体数字掩盖类别之间的差异。

```python
for class_index in range(len(classes)):
    mask = labels == class_index
    per_class_correct[class_index] += (
        predicted[mask] == class_index
    ).sum()
    per_class_total[class_index] += mask.sum()
```

这里的 `mask` 只选出当前类别的样本。某个 batch 没有该类别时，两个增量都为零，不需要额外分支。最终输出时再检查 `per_class_total`，避免空类别造成除零。

### TensorBoard 与模型保存

每轮平均 loss 写到 `runs/lenet_cifar10_task1`，TensorBoard 横轴按 epoch 记录。

```python
avg_loss = running_loss / len(trainloader)
writer.add_scalar("train/epoch_loss", avg_loss, epoch + 1)
```

训练结束后保存的是 `state_dict()`。它只包含参数和 buffer，不包含 Python 类定义、优化器动量与当前 epoch。用于本次测试已经足够；若要从中断处继续训练，还要一起保存 optimizer state 和训练进度。

### 成品代码

最终实现集中在一个 `test.py` 中。文件里只有 `LeNet` 和 `main()` 两个入口：`LeNet.forward()` 返回 logits，`main()` 串起数据、训练、模型保存和测试。完整代码见 [Lab 1 源码](https://github.com/elainafan/Programming-in-AI-2025Fall-PKU/tree/main/Lab1)。

### 实验结果

```bash
python test.py
tensorboard --logdir runs
```

程序训练十轮后保存 `task1_lenet_cifar10.pth`，并输出整体与分类别准确率。两组 loss 曲线使用独立日志记录，分类结果由测试集的 10000 张图像统计得到。

| momentum | 第 1 轮 loss | 第 10 轮 loss | 测试准确率 |
| ---: | ---: | ---: | ---: |
| 0 | 2.2205 | 1.3110 | 55.31% |
| 0.9 | 1.6810 | 0.8443 | 62.98% |

![](assets/labs/lab-01/momentum-loss-curves.png)

![](assets/labs/lab-01/test-accuracy.png)
