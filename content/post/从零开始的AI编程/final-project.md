---
title: 从零开始的 AI 编程大作业
date: 2026-01-17
categories:
    - AI
slug: ai-programming-final-project
hidden: true
seriesOrder: 27
---

# 从零开始的 AI 编程大作业

> [!CAUTION]
>
> **本笔记仅供参考，请勿抄袭。**

## 任务

Final Project 围绕 CIFAR-10 展开，包含三条逐步下沉的训练路径。

1. 用 PyTorch 建立单卡分类基线。
2. 在 PyTorch 中实现数据并行或模型并行。
3. 不使用现成深度学习框架完成模型计算，以 CUDA、pybind11 和 Python 组成自己的训练框架。

Bonus 原题要求把自定义框架扩展到 ImageNet。受显存、训练时间和调试成本限制，实际跑完的是 Tiny ImageNet。两者规模差异很大，因此这里明确记录为 Tiny ImageNet，不把结果写成完整 ImageNet 实验。

## 文件结构

```text
Final_Project/
├── Task1/
│   ├── main.py
│   ├── models.py
│   └── utils.py
├── Task2/
│   ├── main.py
│   ├── models.py
│   └── utils.py
├── Task3/
│   ├── src/
│   ├── mytorch/
│   ├── main.py
│   └── models.py
└── Bonus/
    ├── src/
    ├── mytorch/
    ├── main.py
    └── prepare_tiny_imagenet.py
```

前三部分各自可以独立构建和运行。Task 3 与 Bonus 都有自己的 CUDA 扩展，不能把一个目录生成的 `mytensor` 动态库混到另一个目录中。

## Task 1：PyTorch 基线

### 数据划分

CIFAR-10 的 50000 张训练图像按固定随机种子划分为 45000 张训练样本和 5000 张验证样本。官方 10000 张测试图像只在训练完成、恢复最佳验证模型后评估一次。

训练集使用随机水平翻转和四像素填充后的随机裁剪。验证集与测试集只做张量转换和归一化。另建一份无增强的训练集视图，用于统计可比较的训练准确率。

测试集不参与挑选模型，带随机裁剪的训练图像也不用于统计训练准确率。

### 模型

LeNet 沿用 Lab 1 的两层卷积结构，作为低成本基线。MiniVGG 使用三组双卷积块，通道数依次为 64、128、256，每个卷积后接 Batch Normalization 与 ReLU，每组末尾再池化。最后通过自适应平均池化得到 $256\times1\times1$ 特征，经 dropout 后映射到 10 个类别。

两种模型都使用交叉熵、SGD、动量 0.9 和权重衰减 $5\times10^{-4}$ ，初始学习率为 0.01，并在完整训练周期上做余弦退火。MiniVGG 额外启用自动混合精度。

| 模型 | Epoch | Batch size | 混合精度 |
| --- | ---: | ---: | --- |
| LeNet | 30 | 64 | 否 |
| MiniVGG | 50 | 128 | 是 |

每轮验证准确率提高时才覆盖 `best_model.pth`。最终测试加载最佳检查点，而不是直接使用最后一个 epoch 的参数。

### 结果

| 模型 | 最佳验证准确率 | 测试准确率 | 训练时间 |
| --- | ---: | ---: | ---: |
| LeNet | 70.32% | 70.26% | 1362.27 s |
| MiniVGG | 90.70% | 89.97% | 9769.58 s |

LeNet 与 MiniVGG 的训练损失都持续下降，没有出现数值发散。

![](assets/labs/final-project/task1-lenet-loss.png)

![](assets/labs/final-project/task1-minivgg-loss.png)

MiniVGG 比 LeNet 高出 19.71 个百分点，训练时间约为后者的 7.2 倍。验证与测试准确率相差不到一个百分点，说明验证集挑出的检查点在独立测试集上保持了接近的表现。

```bash
python main.py --model lenet --epochs 30 --batch-size 64 \
  --optimizer sgd --lr 0.01 --output-dir results_lenet

python main.py --model minivgg --epochs 50 --batch-size 128 \
  --optimizer sgd --lr 0.01 --amp \
  --output-dir results_minivgg
```

## Task 2：数据并行

### 训练过程

这一部分选择同步数据并行。每个训练 step 分为四步。

1. 沿 batch 维把输入切分到多张 GPU。
2. 每张 GPU 保存一份模型副本，独立完成前向与反向。
3. 梯度归约到主设备。
4. 主设备上的优化器更新参数，下一步再同步各副本。

代码先把模型移动到主设备，检测到多张 GPU 时才包装 `nn.DataParallel`。

```python
model = model.to(device)
if torch.cuda.device_count() > 1:
    model = nn.DataParallel(model)
```

`DataParallel` 会在参数名外增加 `module.` 前缀。保存与恢复检查点时要取得内部模型对象。

```python
state_dict = (
    model.module.state_dict()
    if isinstance(model, nn.DataParallel)
    else model.state_dict()
)
```

数据划分、增强、损失、SGD 参数与学习率调度都沿用 Task 1。这样才能把训练差异尽量限制在设备并行上。

### 结果边界

| 模型 | 总 batch | GPU 数 | Epoch | 验证准确率 | 测试准确率 | 时间 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| LeNet | 64 | 1 | 30 | 70.32% | 70.26% | 1362.27 s |
| LeNet | 64 | 4 | 30 | 71.08% | 70.90% | 402.50 s |
| MiniVGG | 128 | 1 | 50 | 90.17% | 89.95% | 8528.34 s |
| MiniVGG | 128 | 4 | 50 | 91.66% | 90.48% | 922.58 s |
| MiniVGG | 512 | 4 | 50 | 89.50% | 87.92% | 314.89 s |

单卡与四卡记录来自不同机器，旧日志没有完整留下 GPU 型号、CPU、存储和软件版本。因此，这些时间只能表示当次运行耗时，不能直接计算严格的四卡加速比。

总 batch 保持不变时，单卡与四卡的准确率接近，说明模型复制与梯度归约没有改变训练目标。将 MiniVGG 的 batch 从 128 提到 512 后，时间继续下降，测试准确率却降到 87.92%。每个 epoch 的更新次数变少，而学习率与调度没有同步调整，优化轨迹已经不同。大 batch 的公平比较还需要学习率缩放与 warmup。

```bash
python main.py --model minivgg --epochs 50 \
  --batch-size 128 --amp \
  --output-dir multi_results_minivgg
```

复现计时时，应在同一台机器、相同数据缓存状态下分别限制一张和多张 GPU，并保持总 batch 不变。

## Task 3：自定义框架

### 三层结构

自定义框架分成 CUDA 后端、pybind11 边界和 Python 前端。

| 层次 | 作用 |
| --- | --- |
| CUDA 后端 | Tensor 内存、逐元素运算、矩阵乘、卷积、池化与交叉熵 |
| pybind11 | 暴露 `mytensor`，完成 NumPy 与设备 Tensor 的复制 |
| Python 前端 | 计算图、自动微分、Module、SGD、Adam 与训练循环 |

输入由 torchvision 读取，再通过 NumPy 送入自定义 Tensor。PyTorch 只在测试中生成参考结果，不参与模型前向、反向或参数更新。

后端在 Lab 3、Lab 4 的基础上补充逐元素加减乘除、平方根、reshape、broadcast、summation 和 flatten。矩阵乘使用 cuBLAS，卷积仍由 `im2col`、矩阵乘和 `col2im` 组成。

Python 端的 Tensor 把 CUDA 对象保存在 `cached_data` 中。运算符建立计算图，反向时做拓扑排序与梯度累计；优化器再直接更新参数的缓存数据。

```python
optimizer.zero_grad()
logits = model(images)
loss = cross_entropy(logits, labels)
loss.backward()
optimizer.step()
```

### 模型差异

自定义 LeNet 与 PyTorch 基线一致。MiniVGG 仍有三组双卷积块，但框架没有实现 Batch Normalization，自适应平均池化也改为一次 $4\times4$ 最大池化，将 $256\times4\times4$ 压到 $256\times1\times1$ ，再接线性分类器。

因此，Task 1 与 Task 3 中名为 MiniVGG 的网络并不完全相同，准确率差异不能全部归因于框架执行效率。

### 测试

训练前先构建扩展，再运行前向、数值梯度、拓扑排序和整图反向测试。本次重新构建后共 22 项测试，全部通过。

![](assets/labs/final-project/framework-tests.png)

单元测试覆盖小尺寸算子和计算图。CIFAR-10 的长时间训练又进一步检查了卷积、自动微分与参数更新能否持续协同工作。

### CIFAR-10 结果

| 模型 | Batch | 优化器 | Epoch | 验证准确率 | 测试准确率 | 时间 |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| LeNet | 64 | SGD | 30 | 66.44% | 67.11% | 2172.7 s |
| LeNet | 128 | SGD | 30 | 67.86% | 68.87% | 1312.3 s |
| MiniVGG | 128 | SGD | 50 | 85.80% | 86.12% | 2383.0 s |
| MiniVGG | 256 | SGD | 50 | 84.72% | 84.45% | 1930.1 s |
| MiniVGG | 128 | SGD | 100 | 87.10% | 86.43% | 5063.1 s |
| MiniVGG | 128 | Adam | 50 | 63.38% | 63.05% | 1984.6 s |

![](assets/labs/final-project/custom-minivgg-acc.png)

LeNet 将 batch 从 64 增到 128 后，训练时间减少约 40%，测试准确率提高 1.76 个百分点。MiniVGG 从 50 个 epoch 延长到 100 个 epoch 后，验证准确率继续上升，测试准确率只增加 0.31 个百分点。

Adam 的结果明显低于 SGD，只能说明当前学习率与这套框架中的模型不匹配。它不能概括两种优化器的一般优劣。

自定义框架的主要性能开销来自频繁的 Python/CUDA 边界调用、逐算子同步、结果回传和缺少算子融合。模型侧缺少 Batch Normalization，也限制了 MiniVGG 的训练表现。

```powershell
cmake -S src -B build
cmake --build build --config Release

$env:PYTHONPATH = "$(Resolve-Path build/Release);$PWD"
python check_install.py
python -m pytest -q mytorch

python main.py --cuda --model lenet --optimizer sgd \
  --epochs 30 --batch-size 128 \
  --output-dir result_lenet_SGD_2
```

## Bonus：Tiny ImageNet

Tiny ImageNet 包含 200 个类别，每类 500 张训练图像，分辨率为 $64\times64$ 。它比 CIFAR-10 更难，却仍远小于完整 ImageNet。

官方测试集没有公开标签，代码把带标签的验证集同时交给最终评估接口。两者实际上是同一批数据，因此只报告一次验证准确率，不再列一个假的独立测试准确率。

训练增强包括八像素填充后的随机裁剪、随机水平翻转、ColorJitter，以及 Tiny ImageNet 的通道均值与标准差归一化。验证集只做张量转换与归一化。

基础 MiniVGG 把输入缩放为 $32\times32$ 。MiniVGG64 保留原生分辨率，三次池化后将空间尺寸从 64 降到 8，再加一次池化得到 $256\times4\times4$ ，展平后映射到 200 个类别。

训练使用 batch size 256、SGD 和动量 0.9，共 50 个 epoch，在第 20、40 个 epoch 将学习率乘以 0.1。

| 实验 | 输入 | 初始学习率 | 权重衰减 | 验证准确率 |
| --- | ---: | ---: | ---: | ---: |
| Original | $32\times32$ | 0.01 | $5\times10^{-4}$ | 32.15% |
| MiniVGG64 v1 | $64\times64$ | 0.01 | $5\times10^{-4}$ | 44.93% |
| Final 1 | $64\times64$ | 0.01 | $10^{-3}$ | 45.24% |
| Final 2 | $64\times64$ | 0.02 | $10^{-3}$ | 48.89% |

![](assets/labs/final-project/tiny-imagenet-acc.png)

保留原生分辨率后，MiniVGG64 v1 比 $32\times32$ 基线提高 12.78 个百分点。加入更强的数据增强和学习率衰减后，Final 2 达到 48.89%。

```bash
python prepare_tiny_imagenet.py

python main.py --cuda --dataset tinyimagenet \
  --model minivgg64 --optimizer sgd \
  --epochs 50 --batch-size 256 \
  --lr 0.02 --weight-decay 0.001 \
  --output-dir result_3
```

这组结果说明自定义框架能够处理 200 类和更大的输入，但没有完成原题中的完整 ImageNet。继续扩展前，应先减少 Python 调度与显存开销，增加 Batch Normalization 与检查点保存，并为最终评估准备独立数据集。
