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

## 大作业简要介绍

大作业先用 PyTorch 单卡训练 CIFAR-10，再加入数据并行，最后换成前几次 Lab 搭出的 CUDA Tensor、Python 扩展和自动微分框架。Bonus 原要求完整 ImageNet，本机当时无法承担对应的数据与训练开销，实际完成的是 Tiny ImageNet。

## 在动手之前

Task 1 与 Task 2 共用一套数据划分。训练集参与梯度更新，验证集决定检查点，测试集只在恢复最佳参数后评估。随机增强只放在训练 loader 中，验证和测试使用固定预处理。

数据并行会在多张 GPU 上复制模型，把一个 batch 切成若干份，分别执行前向和反向，再把梯度归约到主设备。模型状态保存时还要处理 `DataParallel` 添加的 `module.` 前缀。总 batch 改变后，每个 epoch 的参数更新次数也会变化，学习率和调度策略不能照搬。

Task 3 会把前六次 Lab 的 Tensor 存储、CUDA 算子、Python 绑定、计算图和优化器全部接起来。模型层组合算子，自动微分按图回传梯度，optimizer 读取参数及其 `grad`。开始完整训练前，需要先把每一层的 shape 和设备传递单独跑通。

Tiny ImageNet 包含 200 个类别，输入分辨率为 $64\times64$ 。分类器输出、预处理统计量和末端空间尺寸都要参数化。官方 test split 没有公开标签，保留日志只能报告验证集准确率，不能把同一批数据同时称作验证与测试。

## 文件结构

四个目录都能独立运行。

```text
Final_Project/
├── Task1/    PyTorch 单卡基线
├── Task2/    PyTorch 数据并行
├── Task3/    自定义训练框架
└── Bonus/    Tiny ImageNet 扩展
```

Task 1 与 Task 2 使用同一套模型和数据划分；Task 3 只借用 torchvision 读取 batch，进入模型前会把它转换为自定义 Tensor。

## Task 1：PyTorch基线

Task 1 分为 `utils.py`、`models.py` 和 `main.py`。

| 文件 | 内容 |
| --- | --- |
| `utils.py` | 随机种子、设备选择、评估和曲线保存 |
| `models.py` | LeNet、MiniVGG 与模型工厂 |
| `main.py` | 数据划分、优化器、调度器、训练和检查点 |

入口参数控制模型、设备、worker 数、AMP、优化器、学习率、batch size 和输出目录。默认训练 30 个 epoch，batch size 为 64；SGD 默认 momentum 为 0.9，weight decay 为 $5\times10^{-4}$ 。命令行解析只发生在 `main()`，模型文件不读取全局参数。

### 数据划分

CIFAR-10 的训练部分按固定随机种子划分为训练集和验证集。代码为同一批训练索引建立两个 Dataset view：带增强的一份用于参数更新，不带增强的一份用于统计训练准确率。

```text
train indices ─┬─ 随机裁剪、翻转 -> trainloader_aug -> 训练
               └─ 固定预处理     -> trainloader_clean -> 评估
val indices ------ 固定预处理     -> valloader
test set --------- 固定预处理     -> testloader
```

若直接在带随机增强的 loader 上报告训练准确率，每个 epoch 看到的图像都不同，数值会额外包含增强噪声。测试集只在恢复最佳验证检查点后使用一次，不参与挑选模型。

代码只生成一次 `train_idx` 和 `val_idx`，两种 transform 再复用这组索引。训练、验证若各自重新划分，同一个样本可能落入不同集合。

实际比例是 45000 张训练、5000 张验证。三个评估 loader 的 batch size 取训练 batch 的两倍，因为它们不保存反向图。训练 loader 开启 shuffle，另外三个保持固定顺序。

```python
train_subset_aug = Subset(full_dataset_aug, train_idx)
train_subset_clean = Subset(full_dataset_clean, train_idx)
val_subset = Subset(full_dataset_clean, val_idx)
```

两个训练子集共用相同 `train_idx`，差别只在 transform。若分别随机划分，固定预处理下的训练准确率便不再对应参与训练的那批图像。

### LeNet 与 MiniVGG

`get_model(name)` 隔离模型创建，训练循环只依赖 `nn.Module` 接口。LeNet 用来快速检查整条流水线，MiniVGG 用三组卷积块承担正式训练。两者都返回 logits，损失函数、优化器和评估函数可以完全复用。

```python
model = get_model(args.model, num_classes=10).to(device)
criterion = nn.CrossEntropyLoss()
```

MiniVGG 启用混合精度时，autocast 只包住前向与损失；梯度缩放由 `GradScaler` 管理。

MiniVGG 每个卷积块为 `Conv2d -> BatchNorm2d -> ReLU`，通道数依次为 64、128、256，每组有两个卷积并在末尾池化。最后用 `AdaptiveAvgPool2d(1)` 压成 $N\times256\times1\times1$ ，再经过 Dropout 和全连接。分类器输入不需要手算空间尺寸；Task 3 没有这层自适应池化，比较两条路径时要把这里单独列出来。

```python
with torch.autocast(
    device_type=device.type,
    enabled=args.amp and device.type == "cuda",
):
    outputs = model(inputs)
    loss = criterion(outputs, labels)

scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

若直接对缩放后的梯度调用普通 `optimizer.step()`，参数会使用错误尺度。AMP 的前向上下文和更新流程必须成套出现。

AMP 关闭时仍然经过同一个 `GradScaler` 对象，只是 `enabled=False`，训练循环无需维护两份 backward 分支。CPU 路径同样会自动关闭，不会误用 CUDA autocast。

### 训练与检查点

`main.py` 每轮按固定顺序执行训练、学习率调度、训练集评估、验证集评估和检查点更新。只有验证准确率提高时才覆盖 `best_model.pth`，最终测试也加载这份参数，不使用最后一个 epoch 的模型。

```text
trainloader_aug -> 参数更新
scheduler.step()
trainloader_clean -> 训练准确率
valloader -> 决定是否保存
训练结束 -> 加载 best_model.pth -> testloader
```

CosineAnnealingLR 的 `T_max` 等于总 epoch 数，每轮结束后调用一次。若把 `scheduler.step()` 放进 batch 循环，学习率会在一轮内走完整条余弦曲线。

检查点只保存 `state_dict`，模型结构仍由 `models.py` 创建。恢复时模型名和类别数必须与保存时一致；当前检查点没有 optimizer、scheduler、scaler 和 epoch，不能接着原来的优化状态续训。

两种模型的 loss 曲线用于检查数据、损失和更新是否接通，具体结果统一放在文末。

## Task 2：数据并行

Task 2 复用 Task 1 的数据、模型、损失和训练循环，只在模型创建后增加一层设备包装。

```python
model = model.to(device)
if torch.cuda.device_count() > 1:
    model = nn.DataParallel(model)
```

每个 step 中，`DataParallel` 沿 batch 维切分输入，在多张 GPU 上复制模型并独立前向、反向，随后把梯度归约到主设备，由同一个 optimizer 更新主副本。训练循环仍只接触普通 `nn.Module` 接口，损失和评估代码不必跟着改。

输入先被送到主设备，再由 `DataParallel` scatter。每张卡获得一个 batch 切片，模型副本只在当次 forward 使用；参数更新仍发生在主副本。batch 小于 GPU 数量时，有些卡几乎拿不到数据，并行开销反而更显眼。

### 检查点

`DataParallel` 会在参数名前增加 `module.`。为了让单卡与多卡检查点互通，保存和加载时都要访问内部模型。

```python
base_model = (
    model.module
    if isinstance(model, nn.DataParallel)
    else model
)
torch.save(base_model.state_dict(), checkpoint_path)
```

当前保存处已经解开 `model.module`，加载处也按包装状态选择目标对象，因此产出的 key 不带 `module.` 前缀。这样同一个检查点可以在单卡和多卡之间来回使用。

### 对照实验

单卡与四卡首先保持相同总 batch，检查准确率与耗时；随后再把四卡 MiniVGG 的总 batch 提高到 512。后一个配置每轮更新次数更少，结果不能只按 GPU 数解释。计时前预热 DataLoader 和 CUDA，并在起止位置同步设备，避免把异步 kernel 留到计时区间之外。

## Task 3：自定义框架

Task 3 把前几次 Lab 的代码组合成五层。

```text
main.py                 训练调度与数据批次
models.py               Module、LeNet、MiniVGG
mytorch/                Tensor、Op、自动微分、优化器
src/tensornn.cu         pybind11 绑定
src/tensor*.{h,cu}      CUDA 存储与算子
```

一个 batch 在 Task 3 中依次经过这些对象。

```text
torch DataLoader
 -> NumPy
 -> mytensor.Tensor
 -> mytorch.Tensor
 -> model forward
 -> cross_entropy
 -> compute_gradient_of_variables
 -> optimizer.step
 -> NumPy 统计
```

`models.py` 调用 `conv2d()`、`relu()` 和 `linear()`，不接触 CUDA 指针；自动微分调用各 Op 的 `gradient()`；Python 绑定负责在 NumPy 与后端 Tensor 间复制；CUDA 层接收形状和裸数据。

代码中同时出现三种 Tensor。

| 层 | 对象 | 保存内容 |
| --- | --- | --- |
| C++ | `mytensor.Tensor` | shape、device、底层存储 |
| 自动微分 | `mytorch.Tensor` | Op、inputs、cached_data、grad |
| 数据入口 | `torch.Tensor` | DataLoader 交出的 batch |

训练入口先把 PyTorch batch 转成 NumPy，再由 `mytensor.Tensor.from_numpy()` 搬到 GPU，最后包进 `mytorch.Tensor` 参与构图。打印或统计时则沿相反方向回到 NumPy。对象名相近，调试时必须先确认当前变量属于哪一层。

### Module 与参数

自定义 `Module` 提供 `forward()`、`parameters()`、`train()` 和 `eval()`。LeNet、MiniVGG 手动创建可求导参数，并在 `parameters()` 中按固定顺序返回。

```python
class Module:
    def parameters(self):
        return []

    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)
```

`Module` 不会自动发现参数。LeNet 的 `parameters()` 手工返回十个 Tensor，顺序是两组卷积权重与偏置、三组全连接权重与偏置；MiniVGG 返回十四个。`to_device()`、`zero_grad()` 和 optimizer 都遍历这份列表，漏掉的参数仍能参与前向，却不会被迁移或更新。

`to_device()` 只迁移 `model.parameters()`，输入则在每个 batch 创建时直接进入目标设备。

自定义 MiniVGG 没有复刻 PyTorch 版的 BatchNorm 与 Dropout，末尾使用 $4\times4$ max-pool 模拟全局池化。两边共享大致的网络骨架和训练任务，但并非逐层等价模型，准确率差异也不能全部归因于后端。

### 前向与反向

模型前向只组合高层算子，输出 Tensor 会记录计算图。损失节点创建后，训练循环显式构造标量梯度种子，再调用图引擎。

```python
logits = model(x)
loss = cross_entropy(logits, y)

optimizer.zero_grad()
compute_gradient_of_variables(loss, Tensor(grad_seed))
optimizer.step()
```

前向调用 Lab 3 的 CUDA 算子，Python 对象经 Lab 4 的绑定进入后端；损失节点交给 Lab 5 的计算图反传，Lab 6 的 optimizer 最后读取参数梯度。`gradient()` 返回的 shape 一旦出错，optimizer 看到的参数梯度也会跟着错位。

CPU 与 CUDA 路径使用不同的标签格式：CPU 使用 one-hot，CUDA 后端接收类别下标，训练入口因此分别构造 `y`。

卷积和全连接的 backward 一次返回多个底层 Tensor。自动微分层用 `Conv2dBackprop` 或 `LinearBackprop` 建立一个结果节点，再通过 `TupleGetItem(0..2)` 取出 $\mathrm{d}X$ 、 $\mathrm{d}W$ 与 $\mathrm{d}b$ 。这样后端只跑一次反向，不会为了三个返回值重复启动整套 kernel。

```python
back_node = Conv2dBackprop(stride, padding)(
    input, weight, bias, out_grad
)
return [
    TupleGetItem(0)(back_node),
    TupleGetItem(1)(back_node),
    TupleGetItem(2)(back_node),
]
```

这些 backward Op 没有实现高阶梯度，`TupleGetItem.gradient()` 也留空，本次训练只使用一阶梯度。

### 训练循环

训练循环负责 batch 转换、前向、反向、更新和统计。每个 batch 末尾显式删除图中对象并触发垃圾回收，避免 Python 引用让整张图长期留在内存中。

```python
del x, y, logits, loss, grad_seed
gc.collect()
```

这是一种保守处理，代价是每个 batch 都会触发一次 Python 垃圾回收。

每次 `.numpy()` 都会同步并复制。训练代码为了统计预测，会把 logits 搬回 Host；若每层都这样查看中间值，GPU 会在每个算子后停下来等 CPU。调试模式可以打印一两个 batch，正式训练只回传 loss 与预测所需的数据。

当前训练会记录 JSON 和曲线，但没有像 Task 1 那样保存最佳参数。

自定义 SGD 按参数对象保存 momentum velocity，Adam 也按参数对象保存各自的 `t`、`m` 和 `v`。参数更新直接替换或原地修改 `cached_data`，不会把 optimizer step 接入计算图。`zero_grad()` 则把每个 `p.grad` 设为 `None`，下一轮反向重新累计。

完整训练前先运行算子与 autodiff 测试，再构造一个卷积节点核对三份梯度 shape，最后让 LeNet 跑两个 batch。

## Bonus：Tiny ImageNet

Bonus 沿用 Task 3 的代码，实际训练 Tiny ImageNet，而非完整 ImageNet。

`prepare_tiny_imagenet.py` 先把验证集按类别重排成 `ImageFolder` 可读取的目录；`utils.py` 提供 Tiny ImageNet loader；`models.py` 增加 200 类输出和适配 64 像素输入的 `MiniVGG64`；`main.py` 根据数据集选择类别数和预处理。

```text
原始验证标注
 -> 按类别整理目录
 -> ImageFolder
 -> 训练/验证 loader
 -> MiniVGG64(num_classes=200)
```

Tiny ImageNet 有 200 类，每类 500 张 $64\times64$ 训练图。预处理改用该数据集的通道均值与标准差，`MiniVGG64` 同时调整末端池化和分类器。验证集原本把图片统一放在 `val/images`，类别信息位于标注文件中；整理脚本按类别创建目录后，`ImageFolder` 才能正常读取标签。

验证集有标签，可以用于调参与报告；Tiny ImageNet 官方 test 目录没有直接提供可用标签，因此这里只报告验证集准确率。

曲线记录的是 Tiny ImageNet 训练。类别数从 10 增至 200 后，分类器输出、标签检查与评估统计都要一并修改。

## 完整代码

完整实现见 [Final Project 源码](https://github.com/elainafan/Programming-in-AI-2025Fall-PKU/tree/main/Final_Project)。四个目录彼此独立：

- `Task1/`：PyTorch 单卡训练，包含 LeNet、MiniVGG、验证集选择和检查点。
- `Task2/`：复用 Task 1 的模型与数据流程，增加 `nn.DataParallel`。
- `Task3/`：使用自定义 CUDA Tensor、计算图、Module 和 optimizer 完成 CIFAR-10 训练。
- `Bonus/`：整理 Tiny ImageNet 数据，扩展到 200 类与 $64\times64$ 输入。

Task 1 与 Task 2 可以直接运行 Python 入口。Task 3 和 Bonus 需要先编译各自的 CUDA 扩展，再运行框架测试；测试通过后才启动完整训练。

## 实验结果

### PyTorch 单卡

PyTorch 单卡结果为：

| 模型 | 最佳验证准确率 | 测试准确率 | 训练时间 |
| --- | ---: | ---: | ---: |
| LeNet | 70.32% | 70.26% | 1362.27 s |
| MiniVGG | 90.70% | 89.97% | 9769.58 s |

![](assets/labs/final-project/task1-lenet-loss.png)

![](assets/labs/final-project/task1-minivgg-loss.png)

### 数据并行

数据并行在相同总 batch 下保持了接近的准确率。四卡 MiniVGG 把总 batch 增至 512 后耗时继续下降，测试准确率同时降至 87.92%，说明大 batch 还需要重新匹配学习率与 warmup。

| 模型 | 总 batch | GPU 数 | 测试准确率 | 时间 |
| --- | ---: | ---: | ---: | ---: |
| LeNet | 64 | 1 | 70.26% | 1362.27 s |
| LeNet | 64 | 4 | 70.90% | 402.50 s |
| MiniVGG | 128 | 1 | 89.95% | 8528.34 s |
| MiniVGG | 128 | 4 | 90.48% | 922.58 s |
| MiniVGG | 512 | 4 | 87.92% | 314.89 s |

### 自定义框架

自定义框架重新构建后通过 22 项算子与自动微分测试。MiniVGG 使用 SGD 训练 100 个 epoch，最终验证准确率为 87.10%，测试准确率为 86.43%。

![](assets/labs/final-project/framework-tests.png)

![](assets/labs/final-project/custom-minivgg-acc.png)

### Tiny ImageNet

Tiny ImageNet 的 Final 2 配置达到 48.89% 验证准确率，训练时间为 6861.9 s。该数字来自带标签的验证集，没有独立测试集结果。

![](assets/labs/final-project/tiny-imagenet-acc.png)

### 短跑验证

完整训练前先跑短流程。

```text
1. Task 1 用少量 batch 跑通数据、模型和检查点
2. Task 2 在相同总 batch 下验证单卡、多卡状态兼容
3. Task 3 先运行算子与自动微分测试
4. Task 3 用 --debug-steps 跑一个短 epoch
5. 再运行完整 CIFAR-10 训练
6. 最后整理 Tiny ImageNet 并检查一个 batch 的形状
```

自定义框架的短跑命令可以先限制 batch 数。

```bash
python main.py --model lenet --cuda --debug-steps 2 \
  --epochs 1 --output-dir debug-run
```

`--debug-steps 2` 在两个 batch 后停下，可以检查输入转换、前向、反向和更新。LeNet 跑通后再换 MiniVGG，最后才启动 Tiny ImageNet。
