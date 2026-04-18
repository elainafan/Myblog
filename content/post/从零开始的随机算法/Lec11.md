---
title: Lecture 11
date: 2026-04-18
encrypt: false
image: "/images/4.jpg"
hidden: true
---
## Balls and Bins

### 问题引入

考虑经典的“球和桶 (Balls and Bins)”模型：

假设有 $m$ 个球， $n$ 个桶。

将每个球依次、独立且均匀地扔到这 $n$ 个桶里。

在随机化算法与数据结构（如哈希表的链地址法冲突分析）中，我们极其关心所有桶中的**最大负载量 (Maximum Load)**。

### 核心定理

**定理**：当球的数量与桶的数量相等，即 $m = n$ 时，**最大负载量**以高概率达到 $\Theta\left(\frac{\ln n}{\ln \ln n}\right)$。

更严格地说，对于任意常数 $\epsilon > 0$：

1. **下界**：最大负载量以高概率 $> (1 - \epsilon)\frac{\ln n}{\ln \ln n}$

2. **上界**：最大负载量以高概率 $< (1 + \epsilon)\frac{\ln n}{\ln \ln n}$

### 概率分析思路

#### 下界转换

要证明最大负载量以高概率 $> (1 - \epsilon)\frac{\ln n}{\ln \ln n}$，等价于证明：

**高概率**下，存在（ $\exists$ ）至少一个桶，其负载量 $> (1 - \epsilon)\frac{\ln n}{\ln \ln n}$。

反过来看，这等价于证明其对立事件的概率极低（**低概率**）：对所有（ $\forall$ ）桶，负载量全部 $< (1 - \epsilon)\frac{\ln n}{\ln \ln n}$。

#### 上界转换

要证明最大负载量以高概率 $< (1 + \epsilon)\frac{\ln n}{\ln \ln n}$，分析方式类似，这等价于证明其对立事件发生概率极低：

**低概率**下，存在（ $\exists$ ）至少一个桶，其负载量 $> (1 + \epsilon)\frac{\ln n}{\ln \ln n}$。

#### Union Bound

在分析各个桶的负载时，我们需要计算多个事件并发（或者是联合）的概率。设 $A_i$ 表示第 $i$ 个桶的负载超过某一阈值的事件。

**独立性假设的不适用**：

我们**不能**直接使用独立事件的交集概率公式：

$$
\Pr\left[\bigcap_i A_i\right] = \prod_i \Pr[A_i] \quad \text{❌ (错误)}
$$

**原因（独立性缺失）**：各个桶中的球的总数加起来必须严格等于总球数 $m$。如果已知某些桶里装了很多球，那么其他桶里球的数量必然会受到影响（变少）。因此，各桶负载情况的事件 $A_i$ 之间**并不独立**（存在负相关）。

**Union Bound (联合界法则)**：

在处理“存在某个桶超载”这样的全集界限问题时，虽然我们没有独立性，但在分析概率上界时，我们可以合法且有效地应用 Union Bound (Boole's inequality)：

$$
\Pr\left[\bigcup_i A_i\right] \le \sum_i \Pr[A_i] \quad \text{✅ (有效)}
$$

通过计算单个桶负载超标的概率 $\Pr[A_i]$，然后乘以桶的总数 $n$，我们就能为全局最大负载超过上界的情形给出一个“低概率”的严格约束。

### 证明进一步拆解

#### 上界二项近似与推导

对于上界证明，我们关心的是**单个桶满载**的概率，即计算 $A_i: \Pr\left[X_i \ge (1 + \epsilon)\frac{\ln n}{\ln \ln n}\right]$，其中 $X_i$ 为第 $i$ 个桶中的球数。

由于每个球落入第 $i$ 个桶的概率是 $1/n$，且有 $n$ 个球独立抛掷，因此 $X_i \sim \text{Binomial}(n, 1/n)$。

根据极限理论，当 $n \to \infty$ 时， $\text{Binomial}(n, 1/n)$ 可以被泊松分布完美近似，即 $X_i \sim \text{Poisson}(\mu)$，这里均值 $\mu = n \cdot (1/n) = 1$。

令阈值 $M = (1 + \epsilon)\frac{\ln n}{\ln \ln n}$。利用泊松分布的尾部概率（或者 Chernoff Bound 对 Poisson 分布的直接放缩）：

$$
\Pr[X_i \ge M] \approx \Pr[\text{Poisson}(1) \ge M] \le \frac{e^{-1} \cdot 1^M}{M!} \le \frac{1}{M!}
$$

利用斯特林公式（Stirling's Approximation）取对数估算 $M!$ 的级数：

$$
\ln(M!) \approx M \ln M - M
$$

将 $M = (1 + \epsilon)\frac{\ln n}{\ln \ln n}$ 代入：

$$
M \ln M \approx (1 + \epsilon)\frac{\ln n}{\ln \ln n} \cdot (\ln \ln n - \ln \ln \ln n) \approx (1 + \epsilon)\ln n
$$

因此， $\ln(M!) > \ln n \Rightarrow M! \gg n$ ，且随着略微放大的 $\epsilon$ ，分母将会是趋近于 $O(n^{1+\epsilon})$ 级别的。所以单个桶超载的概率：

$$
\Pr[X_i \ge M] \le \frac{1}{M!} = o\left(\frac{1}{n}\right)
$$

**利用 Union Bound 终结：**

把上面计算出来的单个桶超载概率套用 Union Bound，我们将所有的 $n$ 个桶加起来，从而证明“存在任何一个桶超载”的全局概率为 0：

$$
\Pr\left[\exists i, X_i \ge (1 + \epsilon)\frac{\ln n}{\ln \ln n}\right] = \Pr\left[\bigcup_{i=1}^n A_i\right] \le \sum_{i=1}^n \Pr[A_i] = n \cdot o\left(\frac{1}{n}\right) = o(1)
$$

这就完美证明了：在高概率下， $n$ 个桶中没有任何一个桶的负载超过 $(1 + \epsilon)\frac{\ln n}{\ln \ln n}$。即所谓的“上界”。

#### 下界独立困境

对于下界证明，我们要证明 $\Pr\left[\forall i, X_i \le (1 - \epsilon)\frac{\ln n}{\ln \ln n}\right]$ 极低。

虽然单个 $X_i \sim \text{Binomial}(n, \frac{1}{n})$，但如前所述，由于 $\sum_i X_i = n$，各个 $X_i$ 之间**不独立**。

这意味着我们不能简单地将概率连乘。我们需要借助巧妙的方法来解除这种耦合。

#### 随机占优

为了处理这种相关性并进行放缩，我们引入 **随机占优（又称统计大于）** 的概念：

- 设 $X$ 和 $Y$ 为两个随机变量。
- 称 $X$ 在统计上大于 $Y$（记为 $X \ge_1 Y$），当且仅当对**任意**实数 $c$，都有累计分布函数满足：

$$
\Pr[X \le c] = F_X(c) \le F_Y(c) = \Pr[Y \le c]
$$

- **性质**：如果 $X \ge_1 Y$ 且 $X' \ge_1 Y'$（这里假设 $X, X'$ 之间以及 $Y, Y'$ 之间的相关性不破坏条件，最简单的情况是独立），那么：

$$
X + X' \ge_1 Y + Y'
$$

#### 泊松近似引理

我们的核心思路是通过放缩（Relaxation），将原来不独立的二项分布转化为独立的泊松分布：

$$
\Pr\left[\forall i, X_i \le c\right] \le A \cdot \Pr\left[\forall i, Y_i \le c\right]
$$

其中，寻找一个常数 $A$，并构造一组**相互独立**的随机变量 $Y_i$。

**引理**：

我们构造独立同分布（i.i.d.）的随机变量 $Y_i \sim \text{Poisson}(m/n)$。在我们的问题中 $m=n$，所以 $Y_i \sim \text{Poisson}(1)$。此时有重要结论：

$$
\Pr\left[\forall i, X_i \le c\right] \le 4 \Pr\left[\forall i, Y_i \le c\right]
$$

**引理证明**：

首先基于泊松分布和多项分布的关系，有一个重要**观察**：独立泊松分布在总和条件下的条件概率，恰好等于球和桶模型中球数的联合概率分布：

$$
\Pr[X_1 = c_1, X_2 = c_2, \cdots] = \Pr\left[Y_1 = c_1, Y_2 = c_2, \cdots \Big| \sum_i Y_i = m\right]
$$

**重要观察的数学推导与证明**：

1. **定义球桶模型分布**：
   原始场景下将 $m$ 个球独立并且均匀地扔进 $n$ 个桶，各个桶的球数 $X_1, X_2, \dots, X_n$ 服从多项分布，其联合概率为：

$$
\Pr[X_1 = c_1, \dots, X_n = c_n] = \frac{m!}{c_1! \dots c_n!} \left(\frac{1}{n}\right)^m
$$

   （必须满足条件 $\sum_{i=1}^n c_i = m$）。

2. **定义相互独立的泊松变量**：
   构造 $n$ 个相互独立的随机变量 $Y_i \sim \text{Poisson}(m/n)$，每个变量的概率分布为：

$$
\Pr[Y_i = c_i] = \frac{e^{-\frac{m}{n}} \left(\frac{m}{n}\right)^{c_i}}{c_i!}
$$

3. **展开条件概率并化简分子**：
   通过全概率公式，我们计算 $Y_1, \dots, Y_n$ 的条件概率：

$$
\Pr\left[Y_1 = c_1, \dots, Y_n = c_n \Big| \sum_{i=1}^n Y_i = m\right] = \frac{\Pr[Y_1 = c_1, \dots, Y_n = c_n]}{\Pr\left[\sum_{i=1}^n Y_i = m\right]}
$$

   因为 $Y_i$ 是相互独立的，其联合概率（分子部分）直接利用单个概率对每一个变量连乘计算：

$$
\prod_{i=1}^n \frac{e^{-\frac{m}{n}} \left(\frac{m}{n}\right)^{c_i}}{c_i!} = \frac{e^{-m} \left(\frac{m}{n}\right)^m}{c_1! \dots c_n!}
$$

4. **根据泊松可加性化简分母**：
   因为 $Y_i \sim \text{Poisson}(m/n)$ 且完全相互独立，所有独立泊松变量之和服从参数之和的泊松分布 $\text{Poisson}(m)$，因此分布的分母概率为：

$$
\Pr\left[\sum_{i=1}^n Y_i = m\right] = \frac{e^{-m} m^m}{m!}
$$

5. **验证比值等价**：
   将化简完成后的分子与分母相除：

$$
\frac{e^{-m} \left(\frac{m}{n}\right)^m}{c_1! \dots c_n!} \times \frac{m!}{e^{-m} m^m} = \frac{m!}{c_1! \dots c_n!} \left(\frac{1}{n}\right)^m
$$

   推导得到的这个最终形式严格等于第 1 步定义的 $X_i$ 多项分布联合概率，**从而这个观察得证。**

基于这段等价观察，我们有以下全概率放缩过程：

<div>
$$
\begin{aligned}
\Pr[\forall i, Y_i \le c] &= \sum_k \Pr\left[\forall i, Y_i \le c \Big| \sum_i Y_i = k\right] \Pr\left[\sum_i Y_i = k\right] \\\\
&\ge \sum_{k \le m} \Pr\left[\forall i, Y_i \le c \Big| \sum_i Y_i = k\right] \Pr\left[\sum_i Y_i = k\right] \\\\
&\ge \Pr\left[\forall i, Y_i \le c \Big| \sum_i Y_i = m\right] \sum_{k \le m} \Pr\left[\sum_i Y_i = k\right] \\\\
&= \Pr[\forall i, X_i \le c] \cdot \Pr\left[\sum_i Y_i \le m\right] \\\\
&\ge \Pr[\forall i, X_i \le c] \cdot \frac{1}{4}
\end{aligned}
$$
</div>

**针对最后推导步骤的详细解释：**

1. **为什么能够限制在 $k \le m$ 并提取出 $= m$ 的条件？（单调性放缩）**
   - 第一步到第二步，我们丢掉了 $k > m$ 的项，只保留 $\sum_{k \le m}$，因为概率都是非负的，所以自然是 $\ge$。
   - **核心物理意义（单调性）**： $\Pr\left[\forall i, Y_i \le c \Big| \sum Y_i = k\right]$ 表示的是“当你正好扔了 $k$ 个球时，没有任何一个桶超载 $c$ 的概率”。
   - 显然，扔的球越少，不超载的概率越大。因此，当 $k \le m$ 时，扔 $k$ 个球不超载的概率，**一定大于等于**扔 $m$ 个球的概率。
   - 算法上就有不等式： $\Pr\left[\cdots \Big| \sum Y_i = k\right] \ge \Pr\left[\cdots \Big| \sum Y_i = m\right]$。将其替换进去并作为一个公因式提出来，就形成了第三行。

2. **多项分布替换：**
   - 提出来的公因式 $\Pr\left[\forall i, Y_i \le c \Big| \sum Y_i = m\right]$，根据我们上文刚证明的“重要观察”，它**严格等于**多项分布的概率 $\Pr[\forall i, X_i \le c]$。
   - 而留在求和号里的 $\sum_{k \le m} \Pr\left[\sum Y_i = k\right]$，指的恰好是“所有独立泊松变量之和不超过 $m$ 的概率”，即定义上的 $\Pr\left[\sum_i Y_i \le m\right]$。

3. **为什么是 $1/4$？（泊松分布的中位数性质）**
   - 我们知道 $\sum_i Y_i \sim \text{Poisson}(m)$（参数和均值均为 $m$ 的泊松分布）。
   - 在概率论中，参数为整数 $m \ge 1$ 的泊松分布，其**中位数大致等于均值**。有一个严格的下界定理： $\Pr[\text{Poisson}(m) \le m] > \frac{1}{2}$ 。
   - 既然这个概率恒大于 $1/2$，我们放宽条件，用一个常数 $1/4$（它必然小于 $1/2$）作为安全的下界去替换它，自然也成立 ($\ge \frac{1}{2} \ge \frac{1}{4}$)。
   - （注：用 $\frac{1}{4}$ 或者有的课件用 $\frac{1}{e}$ 或者 $\frac{1}{2}$ 都可以，其目的仅仅是为了得到一个**常数放缩因子**，不影响大 $O$ 阶的渐进分析。）

**结语**：将上面的链条头尾连起来，移项把右边的 $\frac{1}{4}$ 乘到左边去，即可得到我们引理最开始的核心式子：

$$
\Pr[\forall i, X_i \le c] \le 4 \Pr[\forall i, Y_i \le c]
$$

即我们将不独立的原始分布上限，放缩到了独立泊松分布的 $4$ 倍！

借助这个引理，对于下界证明，问题极大简化：我们**只需要证明**在使用独立的泊松分布时：

$$
\Pr\left[\forall i, Y_i \le (1 - \epsilon)\frac{\ln n}{\ln \ln n}\right] = o(1)
$$

因为 $Y_i$ 之间是完全独立的，我们可以合法地利用连乘直接计算联合概率，从而顺利完成下界极低概率的证明。