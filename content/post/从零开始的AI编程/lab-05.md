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

Lab 5 用 NumPy 搭一个小型自动微分框架。需要补齐十二类算子的前向与梯度，再实现拓扑排序和整图反传。单个公式并不难，难点在于广播后的 shape 怎样还原、同一个节点被多条路径使用时怎样累计梯度，以及 `compute()` 与 `gradient()` 到底应该返回哪一层对象。

```text
Op：一个局部运算的前向与梯度规则
Value / Tensor：数值、来源和梯度
Autodiff：整张计算图的遍历与梯度累计
```

`Op` 保存局部规则，`Value` 记住数值来源，`task2_autodiff.py` 只负责图遍历。图引擎不需要写一长串 `if isinstance(op, ...)`，新算子的梯度都留在各自类里。

## 代码结构

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

`basic_operator.py` 定义 `Op` 和 `Value` 的抽象关系；`task1_operators.py` 提供 Tensor 与各个局部运算；`task2_autodiff.py` 负责拓扑排序和整图反传；`device.py`、`utils.py` 则隔离数组后端与常用构造函数。测试也按同样边界拆成算子前向、局部梯度、拓扑顺序和整图梯度四组。

四个核心文件按这条依赖关系连接。

1. `basic_operator.py`，看一个节点保存哪些字段。
2. `task1_operators.py`，看 Tensor 运算如何创建新节点。
3. `task2_autodiff.py`，看图怎样倒序遍历。
4. `tensor.py`，看最终的 `backward()` 如何把几个模块接起来。

直接从 `compute_gradient_of_variables()` 开始写很容易迷路，因为那时还没有弄清 `cached_data` 是 NumPy 数组，还是计算图里的 Tensor。

## 节点与运算

以 $C=A+B$ 为例，结果节点 $C$ 保存相加后的数组、产生它的 `EWiseAdd`，以及输入节点 $A$ 和 $B$。继续计算 $D=C\times A$ 后，节点引用自然连成一张有向无环图。

```python
class Value:
    op: Optional[Op]
    inputs: List["Value"]
    cached_data: NDArray
    grad: Optional["Value"]
```

用户直接创建的 Tensor 没有 `op`，属于叶节点。运算结果由 `Tensor.make_from_op()` 创建，保存输入和算子，并通过 `realize_cached_data()` 获得前向值。

![Tensor 反向传播中的局部计算](assets/slides/09-tensor-backward.png)

前向值和图关系不能混在一起。`Op.compute()` 只接收底层数组，不应在里面创建新的计算图；`Op.gradient()` 接收 Tensor 与上游梯度，返回各输入对应的 Tensor 梯度。这样数值后端以后可以从 NumPy 换成 CUDA，而图引擎仍然只操作统一的 Value 接口。

## 节点怎样产生

`Value._init()` 是叶节点和运算结果共同经过的入口。若调用端没有显式传入 `requires_grad`，它会查看所有输入；只要有一个输入需要梯度，结果节点也参与反向。

```python
if requires_grad is None:
    requires_grad = any(x.requires_grad for x in inputs)

self.op = op
self.inputs = inputs
self.cached_data = cached_data
self.requires_grad = requires_grad
```

叶节点由 `make_const()` 创建，`op=None`、`inputs=[]`，数组直接放进 `cached_data`。运算结果由 `make_from_op()` 创建；当前实现随后立即调用 `realize_cached_data()`，因此它是一张带缓存的 eager graph，不是等到 `.numpy()` 时才真正计算的 lazy graph。

若结果不需要梯度，`make_from_op()` 会返回 `detach()` 后的常量节点。数值仍然保留，指向输入与算子的图边被切断。优化器更新参数时也利用 `.data` 写回缓存，不把更新本身记录进计算图。

Tensor 的运算符重载只负责选算子。

```python
def __mul__(self, other):
    if isinstance(other, Tensor):
        return EWiseMul()(self, other)
    return MulScalar(other)(self)
```

这样 `a * b`、`a + 2` 与 `a @ b` 最终都会进入 `TensorOp.__call__()`，由它调用当前 Tensor 类型的 `make_from_op()`。`TensorFull` 继承 Tensor 后，组合表达式自然仍然产生 `TensorFull`，不需要给每个算子再写一份版本。

## 添加一个算子

每个算子由类和一个薄包装函数组成。

```python
class EWiseMul(TensorOp):
    def compute(self, a, b):
        return a * b

    def gradient(self, out_grad, node):
        lhs, rhs = node.inputs
        return out_grad * rhs, out_grad * lhs


def multiply(a, b):
    return EWiseMul()(a, b)
```

类保存局部规则，包装函数提供自然的用户接口。Tensor 的 `__mul__`、`__add__` 等魔术方法也只调用这些包装函数，不重复实现计算。

新算子依次检查前向、局部梯度和广播后的 shape。

1. 写 `compute()`，先让前向对拍通过。
2. 写 `gradient()`，确认返回值数量与输入数量一致。
3. 处理广播和批量维，确保梯度恢复到原输入形状。
4. 增加包装函数与 Tensor 运算符入口。
5. 用中心差分检查局部梯度，再接进复合计算图。

`gradient_as_tuple()` 把单个 Tensor、list 和 tuple 统一成 tuple。图引擎因而可以始终按输入顺序迭代，不必为一元与多元算子分两套逻辑。当前 `compute_gradient_of_variables()` 还直接判断返回值类型，若统一调用 `gradient_as_tuple()`，主体会更短，也能检查“返回梯度数是否等于输入数”。

矩阵乘 $Z=XY$ 的局部梯度为

$$
\mathrm{d}X=\mathrm{d}Z Y^\mathsf{T}
$$

$$
\mathrm{d}Y=X^\mathsf{T}\mathrm{d}Z
$$

二维输入可直接套用；批量矩阵乘还会广播前导维，结果梯度需要归约回输入原形状。局部公式正确并不代表实现已经覆盖广播。

## 形状恢复

广播让一个输入元素影响多个输出位置，反向时必须把这些路径的梯度相加。`_sum_to_shape()` 先消去多出的前导维，再沿原形状中长度为 1 的轴求和。

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

例如形状 $(3,1)$ 广播到 $(2,3,4)$ 后，反向需要沿新增的第 0 维和原来为 1 的末维归约。只比较元素总数无法判断该沿哪些轴求和。

以批量矩阵乘为例，`np.matmul` 会自动广播前导 batch 维。

```python
grad_a = _sum_to_shape(
    matmul(out_grad, transpose(b)),
    a.shape,
)
grad_b = _sum_to_shape(
    matmul(transpose(a), out_grad),
    b.shape,
)
```

`transpose()` 默认交换最后两维，正好保留 batch 维。算出局部梯度后再调用 `_sum_to_shape()`，将广播产生的维度归约掉。若先假定输入都是二维矩阵，普通测试会通过，一遇到 batched matmul 就会多出几维梯度。

求和算子的梯度走相反方向。前向删除了哪些轴，反向先用 reshape 补回长度为 1 的维度，再广播到输入形状。转置的梯度使用逆置换，reshape 的梯度恢复原 shape。这些操作本身没有复杂公式，真正容易错的是元数据变换。

例如对 shape 为 $(2,3,4)$ 的输入沿轴 1 求和，输出 shape 是 $(2,4)$ 。反向先把上游梯度 reshape 为 $(2,1,4)$ ，再 broadcast 到 $(2,3,4)$ 。少掉中间的长度 1 维后，NumPy 可能仍允许广播，却会沿错误的轴复制。

## 图遍历

反向传播要求一个节点的所有下游贡献先到齐，再计算它对输入的梯度。`topo_sort_dfs()` 使用后序 DFS：先访问全部输入，最后把当前节点加入列表。

```python
def topo_sort_dfs(node, visited, topo_order):
    visited.add(node)
    for input_node in node.inputs:
        if input_node not in visited:
            topo_sort_dfs(input_node, visited, topo_order)
    topo_order.append(node)
```

这个列表从叶节点排到输出，反向传播时倒序遍历。`visited` 不能省略，同一个 Tensor 可能被多条支路引用；重复加入拓扑序会让它的梯度再次向前传播。

节点按对象身份放进 `visited`。两个内容都为 `[1, 2, 3]` 的 Tensor 仍是两个独立变量，不能因为数值相同而合并；反过来，同一个对象在表达式里出现三次，也只能在拓扑序中出现一次。

递归 DFS 对当前实验足够直观。图很深时会遇到 Python 递归深度限制，完整框架通常改用显式栈或基于入度的遍历。

## 梯度累计

在

$$
y=x^2+x
$$

表达式中的变量 $x$ 同时经过两条路径到达输出。图引擎不能在每条路径上直接覆盖 `x.grad`，而是先为每个节点收集所有上游贡献。

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

轮到一个节点时，它的所有下游已经处理完，可以先求和，再调用局部 `gradient()`。叶节点不再向前传播，但累计结果仍保存在 `.grad`，供优化器读取。

`sum(node_to_output_grads_list[node])` 会从整数 0 开始与 Tensor 相加，因此 Tensor 的 `__radd__` 也必须工作。另一种写法是取列表第一项，再对剩余项逐个相加；这样不依赖 `0 + tensor` 的约定。

标量损失的初始梯度是 1。若输出不是标量，调用者必须传入与输出同形状的 `out_grad`，它表示要计算的 vector-Jacobian product。偷偷假设所有输出都是标量，会让中间节点的调试接口非常受限。

`TensorFull.backward()` 在没有收到 `out_grad` 时创建与输出同 shape 的全一 Tensor。对于标量，这就是熟悉的 1；对于向量，相当于先对所有元素求和再反传。若只想查看向量中某一项对输入的影响，需要显式传入 one-hot 形式的上游梯度。

## 一张共享计算图

用

$$
z=(x y+x)(x-y)
$$

检查整图比只测一条链更有用。左侧括号中的 $x$ 有两条局部贡献，整个左括号又与右括号共同影响输出。反向时，两个括号节点必须先收到输出梯度，随后 $x$ 再汇总三条路径。如果拓扑顺序或累计逻辑有问题，这类共享图通常比长链更早暴露错误。

调试时可以打印节点的 `op`、shape 和贡献列表长度，不必直接打印整块数组。若某个节点本应收到两项却只有一项，问题在图连接；贡献数量正确但值不对，再回到局部 `gradient()`。

## 写算子时踩过的坑

- `compute()` 返回底层数组，`gradient()` 返回 Tensor。两层对象混用会绕过计算图，后续高阶组合便断开。
- 一个算子有几个输入，`gradient()` 就必须返回几个对应梯度。单输入算子也要保持返回协议一致。
- `axes=None`、单个整数和 tuple 的行为要统一，否则 Summation 在前向和反向会解释出不同维度。
- 梯度累计不能依赖原地加法。后端 Tensor 还没有可变写接口时，先保存各条路径的梯度，再统一求和。
- 图节点需要按对象身份去重，不能按数值相等去重。两个值相同的独立 Tensor 仍是不同变量。
- 缓存前向值能避免重复计算，也意味着原地修改输入会让缓存失效。框架尚未定义版本计数时，应避免对参与构图的数组做原地写入。

ReLU 的梯度写成 `out_grad * (a > 0)` 时，比较表达式由 NumPy 立即得到布尔数组，再被包装成不需要梯度的常量。这对一阶导数足够；若继续求高阶导，ReLU 在零点本来就没有普通导数，框架仍需明确自己的约定。

指数与对数的梯度则继续使用 Tensor 运算，例如 `out_grad * exp(a)`。这部分会构造新的计算图，因此测试中可以对一阶梯度再调用 backward，检查高阶组合没有被 NumPy 运算悄悄截断。

## 复验

测试先比较各算子的 NumPy 前向值，再用中心差分检查局部梯度

$$
\frac{\partial f}{\partial x_i}
\approx
\frac{f(x+\varepsilon e_i)-f(x-\varepsilon e_i)}{2\varepsilon}
$$

随后再检查拓扑顺序、共享节点和整图梯度。当前 22 项测试全部通过。

![](assets/labs/lab-05/pytest.png)

```bash
python -m pytest -q
```

中心差分的 $\varepsilon$ 不能无限减小。过大时截断误差明显，过小时浮点舍入会淹没差值；当前测试使用的量级足以检查这些 NumPy 算子。前向失败先看 `compute()`，数值梯度失败再看局部规则，只有组合图失败时才去查拓扑排序与梯度累计。
