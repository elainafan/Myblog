---
title: AI 编译器前端
date: 2025-11-05
categories:
    - AI
slug: ai-programming-compiler-frontend
hidden: true
seriesOrder: 11
---

模型程序包含类、函数和 Python 控制流，硬件执行的则是形状明确的 Tensor 运算与 kernel。编译器前端逐层降低程序表示，同时保持模型原有的数值语义。

![AI 编译器的前端与后端](assets/imported/24.png)

以这段代码为例

```python
def layer(x, weight, bias):
    return torch.relu(x @ weight + bias)
```

前端要识别矩阵乘法、广播加法与 ReLU，确定每条边的类型和形状，检查设备是否一致，再把结构交给优化 pass。处理结束后，后端才决定矩阵乘法调用哪个库、ReLU 是否并入同一个 kernel，以及线程怎样映射。

## 前端与 IR

Intermediate Representation 是编译器内部使用的程序表示。它比 Python 约束更明确，又比机器指令保留更多 Tensor 语义。一个系统通常不只使用一种 IR。

- Graph IR 用节点和边表示算子与 Tensor 依赖，适合跨算子融合、常量传播和生命周期分析。
- Linear IR 把操作排成有序指令，控制流和数据流都已显式化，适合更低层的优化。
- Loop IR 把矩阵乘法、卷积等算子展开为循环、索引和缓冲区访问，便于做 tiling 与并行化。
- Machine IR 接近目标指令，负责寄存器分配、指令选择和最终代码生成。

同一个操作会经过多次 lowering。例如高层 `linear` 可以先拆成矩阵乘法和加法，再降低成块矩阵循环，最后映射到 CUDA thread 与 Tensor Core 指令。每下降一层，表达更接近硬件，也会失去一部分高层信息。

LLVM 用统一低层 IR 连接语言前端和机器后端。MLIR 允许不同 dialect 在同一套基础设施里共存，可以让神经网络算子、线性代数循环、GPU kernel 和 LLVM 指令依次出现。前一层完成适合自己的优化后，再转换到下一层。

XLA 在较高层使用 HLO 一类 Tensor IR 表达算子、shape 和数据依赖，StableHLO 则为不同框架与编译器之间提供较稳定的交换形式。HLO 仍保留矩阵乘法、卷积与 Reduce 等语义，适合先做代数化简、融合和布局传播，再为 CPU、GPU 或加速器生成代码。

TVM 会把高层图表示继续降低到 Tensor 与循环层的 TIR。调度可以改变 tile、循环顺序、并行绑定和存储位置，而不必改写算子的数学定义。TorchInductor 也采用相近思路，把捕获到的 PyTorch 子图分成融合区域，再生成 Triton 或 C++ kernel。几套系统的 IR 名称不同，分层目的相同。高层保留语义，低层暴露硬件执行细节。

### 类型系统与静态分析

类型系统描述每个 value 能承载什么对象。对 Tensor 而言，类型至少包含 dtype、rank、shape、device 与 layout；tuple、标量、可选值和控制流结果也要有对应表示。类型检查先排除不合法程序，静态分析再沿图传播已知信息，为常量折叠、布局选择和内存规划提供条件。

前端拿到 `x @ weight` 时，要先验证两个输入能否相乘。若

$$
x\in\mathbb{R}^{B\times K}
$$

$$
W\in\mathbb{R}^{K\times N}
$$

输出采用 $[B,N]$ 这一 shape。若 `bias` 采用 $[N]$ 这一 shape，广播结果仍为 $[B,N]$ 这一 shape。内维不一致时，错误可以在编译阶段报告，不必等 kernel 真正运行。

静态 shape 的每个维度都是常数，内存大小和循环边界可以提前确定。动态 shape 则用符号维度与约束表示，例如符号 $B$ 满足 $B>0$ 且维度 $K$ 能被 $16$ 整除。编译器可以生成通用实现，也可以为常见尺寸建立多个专用版本，并用 guard 在运行时选择。

dtype 推断同样会影响结果。`float16` 矩阵乘法可能用 `float32` 累加，整数卷积也常使用更宽的 accumulator。若前端只记录输入 dtype，不记录计算 dtype 与输出 dtype，后面的融合可能悄悄改变溢出和舍入行为。

Device 与 layout 也属于类型信息。CPU Tensor 与 CUDA Tensor 不能直接参加同一个普通加法；NCHW 与 NHWC 的逻辑 shape 可以对应同一幅图像，但物理地址计算完全不同。

## 图优化

假设捕获到这样的子图

```text
constant -> reshape ┐
                    ├-> add -> relu -> multiply -> output
input --------------┘
```

其中 `reshape` 的输入和目标形状都在编译期已知。前端可以先执行 `reshape`，把结果直接保存为常量，这就是常量折叠。

![常量折叠](assets/imported/25.png)

推理图中的 Batch Normalization 参数已经固定，也可以折叠进前面的卷积。若卷积输出记为 $y=Wx+b$ 并且 Batch Normalization 在当前通道上执行 $ay+c$ 这一变换，合并后的参数满足

$$
W'=aW
$$

$$
b'=ab+c
$$

这样既删除了一个算子，也省去一次中间 Tensor 的读写。训练阶段的均值和方差随 batch 变化，不能直接使用同一变换。

公共子表达式消除按拓扑序查看节点，可以用算子类型、属性、输入 value 的身份和输出类型构造哈希键。键相同的节点只是候选，还要检查广播、layout、device 与精度语义是否完全一致。确认等价后，后一个节点的用户改为读取前一个结果，重复节点才可以删除。

死代码消除从图输出和有副作用的根节点反向遍历。能够沿依赖边到达的节点被保留，其余纯计算节点不会影响可观察结果，可以从图中移除。若某个调试分支没有连接到输出，也没有写文件或修改状态，它就会在这一步消失。

两项变换都依赖副作用信息。随机数、文件写入、状态更新和 collective communication 即使输入相同，两次执行也可能有意产生不同结果。随机算子若显式携带相同 RNG state，编译器仍要确认状态是否会被消费；只比较张量输入并不足以判定两次调用等价。

代数简化会使用局部恒等式

$$
x+0=x
$$

$$
x\times1=x
$$

$$
\operatorname{transpose}
\left(
\operatorname{transpose}(x)
\right)
=x
$$

![代数简化](assets/imported/47.png)

浮点运算不满足严格结合律。`(a + b) + c` 与 `a + (b + c)` 的舍入结果可能不同，NaN、Inf 和 signed zero 也会让部分恒等变换失效。编译器会根据精度模式与 fast-math 选项决定能否重排。

![公共子表达式消除](assets/imported/50.png)

![死代码消除](assets/imported/52.png)

### 算子融合

GPU 执行 `add`、`relu`、`multiply` 三个独立 kernel 时，中间 Tensor 至少要写回和读出 global memory，三个 kernel 也各自承担 launch overhead。若每个输出元素的索引关系一致，可以让一个 thread 连续完成三步。

![算子融合](assets/imported/27.png)

融合后，中间值有机会留在寄存器中。

```cpp
float value = input[index] + bias[channel];
value = value > 0.0f ? value : 0.0f;
output[index] = value * scale;
```

Producer 直接嵌入 Consumer 的循环称为垂直融合。Element-wise 链最容易这样处理，矩阵乘法的 bias 与激活也经常组成 epilogue。

![基于规则的融合过程](assets/imported/33.png)

多个互不依赖的小算子还可以装进同一个 kernel，由不同 thread 区间分别处理，这称为水平融合。它主要减少启动次数，不一定复用中间数据。

融合并非越多越好。一个很大的 kernel 会占用更多寄存器和 shared memory，降低同时驻留的 block 数；Producer 有多个 Consumer 时，内联还可能重复计算。前端先判断依赖和索引是否允许，后端的资源模型再判断这样做是否划算。

## 布局与内存

### 布局变换

逻辑形状相同的 Tensor 可以采用不同物理布局。图像常见 NCHW 与 NHWC，矩阵还分 row-major、column-major 和分块布局。Tensor Core 对内部排列、对齐和维度倍数也有要求。

![Layout Transformation](assets/imported/39.png)

独立 transpose 会读写整块 Tensor，代价可能比目标算子本身还高。前端会尝试把布局变换推入 Producer 或 Consumer。例如 Consumer 只要改一下索引就能读取转置视图时，没有必要先 materialize 一份连续副本。

`reshape`、`transpose` 和切片常常只修改 shape、stride 与 offset，共享原来的存储。后续算子若只支持 contiguous 输入，才需要真正复制。编译器必须区分 view 与拥有独立存储的 Tensor，否则内存复用会覆盖仍被其他 view 使用的数据。

### 内存规划

Tensor 的生命周期从 Producer 写完开始，到最后一个 Consumer 读完为止。生命周期不重叠的 Tensor 可以复用同一段缓冲区。

![Tensor 生命周期与内存复用](assets/imported/41.png)

假设图里先产生记作 $A$ 的 Tensor，再产生记作 $B$ 的 Tensor，最后产生记作 $C$ 的 Tensor。若 $A$ 在 $C$ 出现前已经没有 Consumer，原先分给 $A$ 的存储就能交给 $C$ 使用。静态内存规划先计算每个 Tensor 的 live interval，再按大小、对齐和设备要求分配 offset。First fit、best fit 与按大小排序的 greedy allocation 都是常见策略。

图中存在并行分支时，拓扑序本身不足以判断生命周期。两个节点虽然在某个串行顺序中前后出现，却可能被放到不同 stream 同时执行，它们的 workspace 不能重叠。

![并行执行中的内存规划](assets/imported/45.png)

训练图还要保存 backward 所需的 activation。前端可以标记哪些值必须保留、哪些值能够重算，后端再据此安排显存。

## Pass 管线

一个 pass 只负责一种变换。常量折叠可能让条件恒定，随后死代码消除删掉未选择的分支；代数简化去掉无效节点后，原本隔开的两个 element-wise 算子又可以融合。优化 pipeline 因此会多轮执行部分 pass，直到图稳定或达到迭代上限。

较常见的顺序是

1. 规范化算子并完成 shape、dtype、device 推断。
2. 折叠常量，传播已知属性。
3. 做代数简化、公共子表达式消除和死代码消除。
4. 选择或传播 layout，寻找融合区域。
5. 分区到目标设备，标出通信边。
6. 计算 Tensor 生命周期并规划内存。

顺序不是固定模板。布局选择会改变融合机会，融合也会改变内存需求；训练图与推理图的安全变换也不同。编译器需要在每次变换后继续验证 IR，而不能只看最终图能否运行。

管线完成后，IR 已经明确每个算子的语义、输入输出类型和设备归属。跨设备边会变成 `Send`、`Recv` 或 collective，能够并行的节点保留独立依赖。这份 IR 是前端交给后端的接口。

前端通常不会决定每个 CUDA block 有多少 thread，也不会直接选择 Tensor Core 指令。这些选择依赖具体 GPU、shape 和存储层次，属于后端调度。前端负责让程序变得清楚、合法并暴露优化机会，后端再把这些机会落实成实际机器代码。

接口中还要保留动态维度、stride、alignment 和 alias 等约束。后端可以为已知 shape 生成专用 kernel，也可以为动态维度生成带边界判断的通用版本；若它改变 Tensor 布局或复用 buffer，则必须遵守前端记录的 view 与生命周期关系。缺少这些 metadata 时，机器代码即使单个算子结果正确，也可能在整图中读错内存。
