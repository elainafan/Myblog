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

## 任务

Lab 1 要用 PyTorch 完成 CIFAR-10 分类。提交代码只有一个 `test.py`，其中要包含数据处理、LeNet、十轮训练、整体准确率、分类别准确率和 loss 曲线，最后再比较 SGD 是否使用 momentum 时的差别。

```text
数据与增强 -> LeNet -> 单个训练 step -> 整轮训练 -> 评估与保存
```

文件不大，还是要把几段代码的边界分开。DataLoader 只交出 batch，`LeNet.forward()` 只返回 logits，训练循环负责求导和更新，测试阶段只统计结果。后面几次 Lab 会逐步重写 Tensor、算子和自动微分，这份 PyTorch 代码正好可以当作接口参照。

## 代码入口

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

漏掉这层保护后，worker 会重新导入并执行整个文件，表现通常不是一条干净的异常，而是重复下载、重复打印或者一直卡在创建 DataLoader 的位置。

## 数据入口

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

训练和测试必须使用两套 transform。若测试集也带随机裁剪，每次评估看到的图像都会变化，准确率便失去了可比性。`DataLoader` 的职责也很单纯：训练 loader 打乱样本，测试 loader 保持固定顺序，两边只向后续模块提供 `(inputs, labels)`。

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

## 模型模块

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

把 shape 顺着 `forward()` 写一遍，最容易发现全连接层输入维数是否算错。

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

`forward()` 的返回值是 logits，末尾不接 Softmax。`CrossEntropyLoss` 已经把 log-softmax 和负对数似然合在一起，再手动做一次 Softmax 会改变损失的输入含义，也让数值稳定性变差。

模型和数据各自只在边界处调用一次 `.to(device)`。层内部不判断 CPU 或 CUDA，这样同一份 `forward()` 可以直接复用在两种设备上。

这份 LeNet 一共有 62006 个可训练参数。规模不大，十轮训练足以看见 loss 明显下降。后面改写 CUDA 算子时，也可以先拿它跑一个 batch，避免一开始就用更深的网络排查问题。

## 训练模块

一个 batch 的训练过程只有四步。

```python
optimizer.zero_grad()
outputs = model(inputs)
loss = criterion(outputs, labels)
loss.backward()
optimizer.step()
```

`zero_grad()` 必须发生在下一次反向传播前。PyTorch 默认累加梯度，漏掉这一步以后，当前 batch 会把前面所有 batch 的梯度一起用于更新。`backward()` 只填写各参数的 `.grad`，真正修改参数的是 `optimizer.step()`，两者也不能颠倒。

训练循环还要明确模型状态。当前 LeNet 没有 Dropout 和 Batch Normalization，忘记 `model.train()` 暂时不会改变结果；养成在 epoch 开始时切回训练状态的习惯，换到 MiniVGG 后才不会沿用测试状态。

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

## 优化器状态

普通 SGD 只看当前梯度。加入动量后，优化器还保存跨 batch 的速度项

$$
v_t=m v_{t-1}+g_t
$$

$$
\theta_t=\theta_{t-1}-\eta v_t
$$

连续几个 batch 的梯度方向接近时，历史项会加快这一方向的移动；梯度来回摆动时，它又能削弱单个 batch 带来的突变。这也说明优化器并非一个无状态函数。重新创建 optimizer 会丢掉动量缓冲区，只保存模型参数也不足以无缝续训。

代码还设置了 `weight_decay=1e-4`。PyTorch 的 SGD 会把参数本身按这个系数加入更新，用来限制权重继续增大。比较 momentum 时，其余参数应保持一致，否则曲线同时混进学习率、正则化和初始化的变化。

比较动量时，网络初始化、数据顺序和随机增强都应使用相同随机种子。原实验只固定了网络结构与训练轮数，因此曲线能说明当次运行的差异，不能当成严格的统计结论。

![](assets/labs/lab-01/momentum-loss-curves.png)

## 评估模块

评估前切换到 `eval()`，并使用 `torch.inference_mode()` 关闭计算图记录。

```python
model.eval()

with torch.inference_mode():
    for inputs, labels in testloader:
        outputs = model(inputs.to(device))
        predicted = outputs.argmax(dim=1)
```

整体准确率只需要累计预测正确的样本数。分类别准确率则为每个标签分别维护 `correct` 和 `total`。这一层统计揭示了整体数字看不到的偏差，例如 `ship`、`truck` 往往比外形相近的动物类别更容易区分。

```python
for class_index in range(len(classes)):
    mask = labels == class_index
    per_class_correct[class_index] += (
        predicted[mask] == class_index
    ).sum()
    per_class_total[class_index] += mask.sum()
```

这里的 `mask` 只选出当前类别的样本。某个 batch 没有该类别时，两个增量都为零，不需要额外分支。最终输出时再检查 `per_class_total`，避免空类别造成除零。

![](assets/labs/lab-01/test-accuracy.png)

这里还有两个容易混淆的状态。`model.eval()` 会改变 Dropout、Batch Normalization 等层的行为，`inference_mode()` 则关闭自动微分；它们解决的问题不同。当前 LeNet 没有这两类层，但保留完整评估模板后，换模型时不会悄悄得到错误结果。

## 日志与检查点

每轮平均 loss 写到 `runs/lenet_cifar10_task1`，TensorBoard 横轴使用 epoch，而不是 batch。

```python
avg_loss = running_loss / len(trainloader)
writer.add_scalar("train/epoch_loss", avg_loss, epoch + 1)
```

训练结束后保存的是 `state_dict()`。它只包含参数和 buffer，不包含 Python 类定义、优化器动量与当前 epoch。用于本次测试已经足够；若要从中断处继续训练，还要一起保存 optimizer state 和训练进度。

## 复验

```bash
python test.py
tensorboard --logdir runs
```

程序训练十轮后保存 `task1_lenet_cifar10.pth`，并输出整体与分类别准确率。复验重点是确认训练 loss 能持续下降、评估阶段不产生梯度，以及动量实验使用相互独立的日志目录和检查点文件。

若 loss 从一开始就停在 $\log 10$ 附近，可以按数据、模型、更新三段检查。先看一批输入的范围和标签，再确认输出 shape 为 $N\times10$ ，最后比较一次 `optimizer.step()` 前后的参数。哪一段没有变化，问题通常就停在哪一段。
