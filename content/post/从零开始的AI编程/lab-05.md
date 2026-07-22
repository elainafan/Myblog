---
title: 从零开始的自动微分
date: 2025-11-30
categories:
    - AI
slug: ai-programming-lab-05
hidden: true
seriesOrder: 25
---

# 从零开始的自动微分

> [!CAUTION]
>
> **本笔记仅供参考，请勿抄袭。**

## 任务

Lab 5 模仿 Needle 的结构，逐步补齐一个小型自动微分框架：先实现运算符前向计算，再写每个运算符的梯度规则，随后对计算图做拓扑排序，最后沿反向拓扑序累计梯度。

这次不依赖 CUDA。数值运算由 NumPy 完成，Tensor 保存计算图关系。任意组合出来的表达式都要沿同一套图结构反向传播。

## 文件结构

```text
Lab5/
├── basic_operator.py
├── device.py
├── task1_operators.py
├── task2_autodiff.py
├── tensor.py
├── utils.py
├── test_task1_forward.py
├── test_task1_backward.py
├── test_task2_topo_sort.py
└── test_task2_auto_diff.py
```

- `Value` 表示计算图中的节点。
- `Op` 表示产生节点的运算。
- `Tensor` 保存数值缓存、输入节点与梯度。
- `task1_operators.py` 实现前向与局部梯度。
- `task2_autodiff.py` 负责整张图的反向传播。

## 计算图

以 $C=A+B$ 为例， $A$ 和 $B$ 是输入节点，`EWiseAdd` 是操作， $C$ 保存该操作以及两个输入。继续计算 $D=C\times A$ 时，新节点 $D$ 又会记录乘法操作和输入 $C$ 、 $A$ 。整个表达式自然形成一张有向无环图。

```python
class Value:
    op: Optional[Op]
    inputs: List["Value"]
    cached_data: NDArray
    grad: Optional["Value"]
```

用户直接创建的 Tensor 没有 `op`，属于叶节点。运算产生的 Tensor 则通过 `Tensor.make_from_op()` 记录来源，并按需计算 `cached_data`。

训练通常从一个标量损失反传到大量参数。反向模式自动微分从输出端给定一个伴随值，沿图计算 vector-Jacobian product，不需要显式保存完整雅可比矩阵。矩阵乘节点也只需使用输入、权重和上游梯度，得到形状分别与两项输入一致的梯度。

![Tensor 反向传播中的局部计算](assets/slides/09-tensor-backward.png)

前向值和计算图要分清。`compute()` 只接收 NumPy 数组并返回 NumPy 数组；`gradient()` 接收 Tensor，因为梯度本身还可能参与后续运算并继续构图。

## 运算符

实现的操作包括逐元素加、乘、除、幂，标量运算，矩阵乘，转置，reshape，广播，求和，取负，对数，指数和 ReLU。

每个运算符都要回答两个问题：

1. 给定输入数据，前向值怎么计算。
2. 给定上游梯度，如何得到每个输入的梯度。

逐元素乘法的实现很直接。

```python
class EWiseMul(TensorOp):
    def compute(self, a, b):
        return a * b

    def gradient(self, out_grad, node):
        lhs, rhs = node.inputs
        return out_grad * rhs, out_grad * lhs
```

矩阵乘法 $Z=XY$ 的梯度为

$$
\mathrm{d}X=\mathrm{d}Z Y^\mathsf{T}
$$

$$
\mathrm{d}Y=X^\mathsf{T}\mathrm{d}Z
$$

二维矩阵直接套公式即可，批量矩阵乘还要处理前导维广播。结果梯度可能比原输入多出若干维，最终必须归约回输入形状。

## 广播与求和

广播不会复制逻辑上的变量，却会让一个输入元素影响多个输出位置。反向传播时，这些位置的梯度必须相加。

若输入形状为 $(3,1)$ ，广播到 $(2,3,4)$ ，需要沿新增的第 0 维和原来长度为 1 的末维求和。`_sum_to_shape()` 分两步处理：

1. 先消去比目标多出的前导维。
2. 再沿目标形状中长度为 1 的轴求和，并保留维度。

```python
def _sum_to_shape(tensor, shape):
    while len(tensor.shape) > len(shape):
        tensor = summation(tensor, axes=(0,))

    axes = tuple(
        i for i, (src, dst) in enumerate(zip(tensor.shape, shape))
        if dst == 1 and src != 1
    )
    if axes:
        tensor = summation(tensor, axes=axes).reshape(shape)
    return tensor
```

求和的梯度正好相反。前向删除了哪些轴，反向就先把这些长度为 1 的维度补回来，再广播到输入形状。reshape 的梯度恢复原形状，transpose 的梯度使用逆置换。

这部分最适合用数值梯度检查。形状看似正确并不代表归约轴正确，特别是 batch 维与广播维同时出现时，手算一个小例子往往比盯着代码有效。

## 拓扑排序

反向传播要求一个节点的所有下游贡献先到齐，再计算它对输入的梯度。从输出节点开始做后序 DFS，访问完全部输入后才把当前节点加入列表，得到从叶节点到输出节点的拓扑序。

```python
def topo_sort_dfs(node, visited, topo_order):
    visited.add(node)
    for input_node in node.inputs:
        if input_node not in visited:
            topo_sort_dfs(input_node, visited, topo_order)
    topo_order.append(node)
```

`visited` 不能省略。同一个节点可能被多条支路引用，若重复加入拓扑序，它的梯度会被再次传播。

反向传播时逆序遍历列表。输出节点最先处理，叶节点最后处理。

## 梯度累计

考虑

$$
y=x^2+x
$$

$x$ 同时经过平方支路和恒等支路到达输出。反向传播到 $x$ 时，应得到两条路径贡献之和，而不是保留最后一次写入的梯度。

实现用字典为每个节点保存一组尚未合并的梯度。轮到该节点时，先对列表求和并写入 `node.grad`，再调用当前操作的 `gradient()`。

```python
node_to_output_grads_list[output_tensor] = [out_grad]

for node in reversed(find_topo_sort([output_tensor])):
    node.grad = sum(node_to_output_grads_list[node])
    if node.op is None:
        continue

    input_grads = node.op.gradient(node.grad, node)
    for input_node, input_grad in zip(node.inputs, input_grads):
        node_to_output_grads_list.setdefault(input_node, []).append(input_grad)
```

梯度字典保存列表而非不断原地相加，也避免了某些 Tensor 后端没有实现可变更新的问题。叶节点不再向前传播，但它的累计梯度仍保存在 `grad` 中，供优化器读取。

标量损失通常用全一 Tensor 作为初始梯度。若输出不是标量，则需要显式传入与输出同形状的 `out_grad`，这相当于计算一个向量与输出雅可比的乘积。

## 测试

测试分成四组。

- 前向结果与 NumPy 直接计算比较。
- 使用中心差分检查各运算符的梯度。
- 检查拓扑序中的依赖关系。
- 构造含分支的计算图，验证梯度累计与整图反向传播。

中心差分近似为

$$
\frac{\partial f}{\partial x_i}
\approx
\frac{f(x+\varepsilon e_i)-f(x-\varepsilon e_i)}{2\varepsilon}
$$

它不依赖手写梯度公式，适合发现转置、广播归约和符号错误。测试还覆盖了批量矩阵乘与高阶组合表达式。

本次复验运行 22 项测试，全部通过。

![](assets/labs/lab-05/pytest.png)

## 运行

```bash
python -m pytest -q
```

调试时可以按阶段拆开运行。

```bash
python -m pytest -q test_task1_forward.py
python -m pytest -q test_task1_backward.py
python -m pytest -q test_task2_topo_sort.py
python -m pytest -q test_task2_auto_diff.py
```

先让单个运算符通过前向与数值梯度，再检查整张图，定位会轻松许多。若自动微分测试失败而局部梯度都正确，优先检查拓扑序、共享节点去重和梯度累计。
