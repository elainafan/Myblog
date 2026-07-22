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

Lab 1 要用 PyTorch 跑通 CIFAR-10 分类：准备数据、搭建 LeNet、完成训练与测试，再比较 SGD 是否使用动量时的收敛情况。代码虽然只有一个 `test.py`，实现时仍然可以把它看成五个彼此独立的部分。

```text
数据与增强 -> LeNet -> 单个训练 step -> 整轮训练 -> 评估与保存
```

数据模块决定输入的分布；模型只负责把图像变成 logits；训练循环连接损失函数和优化器；评估代码不参与求导；日志与检查点则负责留下可复验的结果。把这些职责分清以后，更换网络、优化器或数据增强都不必重写整条流程。

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

Windows 下使用多个 DataLoader worker 时，程序入口需要放在

```python
if __name__ == "__main__":
    main()
```

之内，否则子进程会再次执行整个文件，常见表现是重复下载数据、重复创建 worker，甚至直接卡住。

## 模型模块

LeNet 由两组卷积、池化和三层全连接组成

$$
3\xrightarrow{5\times5\ \mathrm{Conv}}6
\xrightarrow{2\times2\ \mathrm{MaxPool}}6
\xrightarrow{5\times5\ \mathrm{Conv}}16
\xrightarrow{2\times2\ \mathrm{MaxPool}}16
$$

空间尺寸按下面的顺序变化

$$
32\to28\to14\to10\to5
$$

最后一组特征图共有 16 个通道，展平后得到 400 个特征。

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

![](assets/labs/lab-01/test-accuracy.png)

这里还有两个容易混淆的状态。`model.eval()` 会改变 Dropout、Batch Normalization 等层的行为，`inference_mode()` 则关闭自动微分；它们解决的问题不同。当前 LeNet 没有这两类层，但保留完整评估模板后，换模型时不会悄悄得到错误结果。

## 复验

```bash
python test.py
tensorboard --logdir runs
```

程序训练十轮后保存 `task1_lenet_cifar10.pth`，并输出整体与分类别准确率。复验重点是确认训练 loss 能持续下降、评估阶段不产生梯度，以及动量实验使用相互独立的日志目录和检查点文件。
