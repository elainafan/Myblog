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

Lab 7 用三条路径训练 CIFAR-10：先写一个 PyTorch 单卡基线，再加入数据并行，最后把训练切换到前几次 Lab 搭出的 CUDA Tensor、Python 扩展和自动微分框架。Bonus 将同一套自定义框架扩展到 Tiny ImageNet。

四个目录都能独立运行。

```text
Final_Project/
├── Task1/    PyTorch 单卡基线
├── Task2/    PyTorch 数据并行
├── Task3/    自定义训练框架
└── Bonus/    Tiny ImageNet 扩展
```

三条路径逐层替换实现，同时保持相同的训练目标。Task 1 提供可信参照；Task 2 只改变设备调度；Task 3 再把模型、算子、梯度与优化器换成自己的代码。某一层出错时，可以退回上一条路径判断问题属于数据、模型还是框架。

## PyTorch 基线

Task 1 分为 `utils.py`、`models.py` 和 `main.py`。

| 模块 | 职责 |
| --- | --- |
| `utils.py` | 随机种子、设备选择、评估和曲线保存 |
| `models.py` | LeNet、MiniVGG 与模型工厂 |
| `main.py` | 数据划分、优化器、调度器、训练和检查点 |

### 数据路径

CIFAR-10 的训练部分按固定随机种子划分为训练集和验证集。代码为同一批训练索引建立两个 Dataset view：带增强的一份用于参数更新，不带增强的一份用于统计训练准确率。

```text
train indices ─┬─ 随机裁剪、翻转 -> trainloader_aug -> 训练
               └─ 固定预处理     -> trainloader_clean -> 评估
val indices ------ 固定预处理     -> valloader
test set --------- 固定预处理     -> testloader
```

若直接在带随机增强的 loader 上报告训练准确率，每个 epoch 看到的图像都不同，数值会额外包含增强噪声。测试集只在恢复最佳验证检查点后使用一次，不参与挑选模型。

数据索引和 transform 应分开保存。只固定 `random_split` 的种子还不够；若训练、验证各自重新划分一次，同一个样本可能落入不同集合。

### 模型接口

`get_model(name)` 隔离模型创建，训练循环只依赖 `nn.Module` 接口。LeNet 用来快速检查整条流水线，MiniVGG 用三组卷积块承担正式训练。两者都返回 logits，损失函数、优化器和评估函数可以完全复用。

模型工厂还让命令行参数不必散落在训练代码中。

```python
model = get_model(args.model, num_classes=10).to(device)
criterion = nn.CrossEntropyLoss()
```

MiniVGG 启用混合精度时，autocast 只包住前向与损失；梯度缩放由 `GradScaler` 管理。

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

### 训练调度

`main.py` 每轮按固定顺序执行训练、学习率调度、训练集评估、验证集评估和检查点更新。只有验证准确率提高时才覆盖 `best_model.pth`，最终测试也加载这份参数，不使用最后一个 epoch 的模型。

检查点只保存 `state_dict`，模型结构仍由 `models.py` 创建。恢复时模型名和类别数必须与保存时一致。若以后需要真正续训，还应一并保存 optimizer、scheduler、scaler 和当前 epoch；仅保存参数只能用于推理或重新开始优化。

两种模型的 loss 曲线在这里充当流水线体检。持续下降说明数据、损失和更新至少能接通，不需要把每次运行的硬件耗时写进实现笔记。

![](assets/labs/final-project/task1-lenet-loss.png)

![](assets/labs/final-project/task1-minivgg-loss.png)

## 数据并行

Task 2 复用 Task 1 的数据、模型、损失和训练循环，只在模型创建后增加一层设备包装。

```python
model = model.to(device)
if torch.cuda.device_count() > 1:
    model = nn.DataParallel(model)
```

每个 step 中，`DataParallel` 沿 batch 维切分输入，在多张 GPU 上复制模型并独立前向、反向，随后把梯度归约到主设备，由同一个 optimizer 更新主副本。训练循环仍看到一个普通 `nn.Module`，这正是模块化带来的好处：并行策略改变了，损失和评估代码不必跟着改。

### 包装后的状态

`DataParallel` 会在参数名前增加 `module.`。为了让单卡与多卡检查点互通，保存和加载时都要访问内部模型。

```python
base_model = (
    model.module
    if isinstance(model, nn.DataParallel)
    else model
)
torch.save(base_model.state_dict(), checkpoint_path)
```

这个兼容处理应收进单独的 checkpoint helper，保存和加载共用同一处判断。以后替换成 DistributedDataParallel 时，只需要改 helper。

### 并行实验的坑

- 对比单卡与多卡时，总 batch size 应保持一致。若每卡 batch 不变，总 batch 会随 GPU 数增长，优化轨迹也随之变化。
- 大 batch 减少每个 epoch 的更新次数，学习率和 warmup 往往需要一起调整，不能把速度变化全归因于并行。
- CUDA kernel 是异步的，计时前后要同步设备。数据缓存、存储速度和不同机器也会污染耗时对比。
- `DataParallel` 每轮都在主进程散射与归约，适合完成接口实验；正式多卡训练通常使用一进程一卡的 DistributedDataParallel。

这部分的验收重点是单卡、多卡能读取同一检查点，并在相同总 batch 下保持接近的验证行为。

## 自定义框架

Task 3 把前几次 Lab 的代码组合成五层。

```text
main.py                 训练调度与数据批次
models.py               Module、LeNet、MiniVGG
mytorch/                Tensor、Op、自动微分、优化器
src/tensornn.cu         pybind11 边界
src/tensor*.{h,cu}      CUDA 存储与算子
```

一次 batch 会沿这条路径往返。

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

每一层只认识紧邻的接口。`models.py` 调用 `conv2d()`、`relu()`、`linear()`，不接触 CUDA 指针；自动微分只调用各 Op 的 `gradient()`；Python 绑定负责在 NumPy 与后端 Tensor 间复制；CUDA 层只接收形状和裸数据。

### Module 与参数

自定义 `Module` 提供 `forward()`、`parameters()`、`train()` 和 `eval()`。LeNet、MiniVGG 手动创建可求导参数，并在 `parameters()` 中按固定顺序返回。

```python
class Module:
    def parameters(self):
        return []

    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)
```

手动列参数能让小框架先跑起来，也很容易漏掉新加的一层。更完整的做法是让 Module 自动注册成员中的 Tensor 和子 Module，再递归收集参数。优化器、设备迁移和检查点都可以共用这份注册表。

`to_device()` 只迁移 `model.parameters()`。输入在每个 batch 创建时直接进入目标设备，二者职责分开。若以后加入 Batch Normalization 的 running statistics 等非参数状态，还需要单独的 buffer 注册机制。

### 前向与反向

模型前向只组合高层算子，输出 Tensor 会记录计算图。损失节点创建后，训练循环显式构造标量梯度种子，再调用图引擎。

```python
logits = model(x)
loss = cross_entropy(logits, y)

optimizer.zero_grad()
compute_gradient_of_variables(loss, Tensor(grad_seed))
optimizer.step()
```

这段流程把 Lab 3 的算子、Lab 4 的绑定、Lab 5 的计算图和 Lab 6 的优化器串在一起。任一算子的 `gradient()` 返回形状不对，错误都会在 optimizer 读取参数梯度前传开；因此框架测试必须先于完整训练。

![](assets/labs/final-project/framework-tests.png)

CPU 与 CUDA 路径目前对标签格式的约定不同：CPU 使用 one-hot，CUDA 后端接收类别下标。训练入口为两条路径分别构造 `y`。这个分支能工作，却把后端细节泄漏到了调度层。更稳妥的接口是让 `cross_entropy` 统一接收类别下标，再由各后端自己转换。

### 训练过程

训练循环负责 batch 转换、前向、反向、更新和统计。每个 batch 末尾显式删除图中对象并触发垃圾回收，避免 Python 引用让整张图长期留在内存中。

```python
del x, y, logits, loss, grad_seed
gc.collect()
```

这是一种保守处理。若 Value、Op 和输入节点形成引用环，频繁 `gc.collect()` 会掩盖生命周期设计问题，也带来明显开销。应通过内存曲线确认是否真的有泄漏，再决定是断开图引用、实现 `detach()`，还是保留周期性回收。

当前训练会记录 JSON 和曲线，但没有像 Task 1 那样保存最佳参数。若要把自定义框架用于长时间训练，参数序列化和恢复是比继续调准确率更优先的模块。

![](assets/labs/final-project/custom-minivgg-acc.png)

### 框架里的坑

- Python Tensor、`mytorch.Tensor` 和 C++ Tensor 是三个对象层次，调试时先确认手里的 `.cached_data` 属于哪一层。
- 设备迁移不能只改标签，必须复制底层存储；参数列表也不能漏掉任何可训练 Tensor。
- 每次 `.numpy()` 都会同步并复制。训练中只在统计确有需要时回传标量或预测结果。
- `train()`、`eval()` 目前只是状态接口。加入 Dropout、Batch Normalization 后，具体层必须真正读取该状态。
- MiniVGG 的自定义版本没有完整复刻 PyTorch 版的所有层，因而只能比较训练链路，不能把差异全部解释成后端性能。
- 计算图与 optimizer state 都跨越模块边界，检查点若只保存参数，无法恢复一次中断的训练。

## Tiny ImageNet

Bonus 沿用 Task 3 的五层结构，只扩展数据和模型边界。实际完成的是 Tiny ImageNet，而非完整 ImageNet。

`prepare_tiny_imagenet.py` 先把验证集按类别重排成 `ImageFolder` 可读取的目录；`utils.py` 提供 Tiny ImageNet loader；`models.py` 增加 200 类输出和适配 64 像素输入的 `MiniVGG64`；`main.py` 根据数据集选择类别数和预处理。

```text
原始验证标注
 -> 按类别整理目录
 -> ImageFolder
 -> 训练/验证 loader
 -> MiniVGG64(num_classes=200)
```

这里最需要守住的是输入契约。把 64 像素图像裁到 32 像素可以复用 CIFAR-10 模型，却损失大量空间信息；保留 64 像素又会改变展平后的特征尺寸。模型不能只把输出类别从 10 改成 200，还要重新核对每次池化后的空间大小和分类器输入维度。

验证集有标签，可以用于调参与报告；Tiny ImageNet 官方 test 目录没有直接提供可用标签，不能把验证集复制一份后同时称作验证和独立测试。数据模块应明确返回哪些 split，训练入口也不应假装存在未加载的测试标签。

![](assets/labs/final-project/tiny-imagenet-acc.png)

Tiny ImageNet 的曲线只用于确认扩展后的数据、模型和后端可以共同训练。它暴露出的显存、数据加载和收敛问题，比一个孤立的最终数字更值得保留。

## 复验顺序

不要一上来运行完整训练。按模块逐层验收更容易定位问题。

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

这套顺序把错误限制在刚接入的模块里。只有短路径稳定后再增加模型规模和数据量，调试时间才不会被完整训练吞掉。
