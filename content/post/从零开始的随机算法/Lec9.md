---
title: Lecture 9
date: 2026-04-18
encrypt: false
image: "/images/2.png"
hidden: true
---
## Chernoff Bounds

本节详细介绍随机算法分析中非常核心的理论：**切尔诺夫界（Chernoff Bounds）**。

它用于给出一组独立随机变量之和偏离其期望值的概率的**指数级衰减上界**。

通过提供极高置信度的误差衰减保证，切尔诺夫界在随机抽样、错误降低（Error Reduction）等算法分析中具有不可或缺的地位。

### 核心定理

**精确界**： 设 $X_1, \cdots, X_n$ 为独立且取值在连续或离散的 $[0, 1]$ 之间的随机变量，设 $E[X_i] = p_i$。

记 $X = \sum_{i=1}^n X_i$，其总体期望为 $\mu = \mathbb{E}[X] = \sum_{i=1}^n p_i$，整体平均概率令为 $p = \frac{\mu}{n}$。

对于偏离期望 $\mu$ 的绝对值 $\lambda$，成立以下上界：

**上界界 (Upper)**： 对于 $0 < \lambda < n - \mu$：

$$
\text{Pr}[X \ge \mu + \lambda] \le \exp\left(-n H_p\left(p + \frac{\lambda}{n}\right)\right)
$$

**下界界 (Lower)**： 对于 $0 < \lambda < \mu$：

$$
\text{Pr}[X \le \mu - \lambda] \le \exp\left(-n H_{1-p}\left(1 - p + \frac{\lambda}{n}\right)\right)
$$

**KL 散度：** 

上述公式中的 $H_p(x)$ 即微相对熵（KL 散度），常记为 $D_{KL}(x || p)$ ：

$$
H_p(x) = x \ln\left(\frac{x}{p}\right) + (1 - x)\ln\left(\frac{1 - x}{1 - p}\right)
$$

### MGF 方法证明

切尔诺夫界的核心依赖于引入**矩生成函数 (Moment Generating Function)** 和马尔可夫不等式。

为了证明上界（即 $\text{Pr}[X \ge \mu + \lambda]$ ）：

$$
\text{Pr}[X \ge \mu + \lambda] = \text{Pr}[e^{tX} \ge e^{t(\mu + \lambda)}] \quad (t > 0)
$$

应用马尔可夫不等式，我们得到：

$$
\text{Pr}[e^{tX} \ge e^{t(\mu + \lambda)}] \le \frac{\mathbb{E}[e^{tX}]}{e^{t(\mu + \lambda)}}
$$

因为变量彼此独立，能够分离乘积项：

$$
\mathbb{E}[e^{tX}] = \mathbb{E}\left[\exp\left(t\sum_{i=1}^n X_i\right)\right] = \prod_{i=1}^n \mathbb{E}[e^{tX_i}]
$$

因为 $X_i \in [0, 1]$ 且 $E[X_i] = p_i$，通过凸性放缩有 $\mathbb{E}[e^{tX_i}] \le p_i e^t + (1 - p_i) = 1 + p_i(e^t - 1)$。

又根据不等式 $1 + x \le e^x$，我们将其放缩至指数上：

$$
\mathbb{E}[e^{tX_i}] \le \exp\left(p_i(e^t - 1)\right)
$$

将其代回乘积式中，并利用期望公式求和：

$$
\mathbb{E}[e^{tX}] \le \prod_{i=1}^n \exp\left(p_i(e^t - 1)\right) = \exp\left(\sum_{i=1}^n p_i (e^t - 1)\right) = \exp\left(\mu(e^t - 1)\right)
$$

现在将这一结果代回到最开始的马尔可夫不等式放缩中：

$$
\text{Pr}[X \ge \mu + \lambda] \le \frac{\exp\left(\mu(e^t - 1)\right)}{\exp\left(t(\mu + \lambda)\right)} = \exp\left(\mu(e^t - 1) - t(\mu + \lambda)\right)
$$

由于此不等式对所有 $t > 0$ 都成立，为了得到最紧密的上界（Tightest Bound），我们对该式的指数部分关于 $t$ 求导并令其等于 $0$。

解得最优点为 $t = \ln\left(1 + \frac{\lambda}{\mu}\right)$。

回代化简整理后就给出了基于 KL 散度的界，以及进一步放缩得到的推论。

### 加法界

通过对核心定理的指数部分求导比较和放缩，能消去复杂形式，得到关于绝对误差 $\lambda$ 和样本数 $n$ 的结果：

$$
\text{Pr}[X \le \mu - \lambda] \le \exp\left(-\frac{2\lambda^2}{n}\right)
$$

$$
\text{Pr}[X \ge \mu + \lambda] \le \exp\left(-\frac{2\lambda^2}{n}\right)
$$

> **核心内涵**：直接表明，偏离其期望 $\mu$ 的概率，随着偏离幅度 $\lambda$ 的平方呈迅速衰减。

### 乘法界

在应用时，不关注绝对偏差而更关注相对比例 $\beta$ 。

即实际在此刻处于 $(1 \pm \beta)\mu$ 范围外的尾部概率，下面是**最常用**界：

设 $\beta$ 为偏离比例：

**下界 $\le (1 - \beta)\mu$**： 对于 $0 < \beta < 1$

$$
\text{Pr}[X \le (1 - \beta)\mu] \le \exp\left(-\frac{\beta^2 \mu}{2}\right)
$$

**上界 $\ge (1 + \beta)\mu$**： 对于 $\beta > 0$

$$
\text{Pr}[X \ge (1 + \beta)\mu] \le 
\begin{cases} 
\exp\left(-\frac{\beta^2 \mu}{2 + \beta}\right) & (\text{当 } \forall \beta > 0) \\ 
\exp\left(-\frac{\beta^2 \mu}{3}\right) & (\text{当 } 0 < \beta \le 1 \text{时})
\end{cases}
$$

### Hoeffding 界

在此前的推论中，变量紧约束在 $[0, 1]$。

若独立随机变量 $X_i$ 取值于各种有界广义区间 $[a_i, b_i]$，能引申出 **Hoeffding 不等式**：

$$
\text{Pr}[X \le \mu - \lambda] \le \exp\left(-\frac{2\lambda^2}{\sum_{i=1}^n (b_i - a_i)^2}\right)
$$

$$
\text{Pr}[X \ge \mu + \lambda] \le \exp\left(-\frac{2\lambda^2}{\sum_{i=1}^n (b_i - a_i)^2}\right)
$$

> **放宽理解**：指数分母不再是固定项，而是所有偏差点平方之和 $\sum (b_i - a_i)^2$。

### 错误降低

假设有一枚有偏硬币，或者一个用来做判定的随机算法。已知单次独立的实验得到正确结果（如正面）的概率 $\ge 3/4$。

如果要进一步降低错误率，我们通过进行 **奇数次 ($2m+1$) 多数表决**。

出现不超过 $m$ 个正面（即依靠大多数表决依然给出了**错误结果**）的概率上限：

$$
\text{Pr}[\text{正确}] \ge 3/4 \implies \text{Pr}[\le m \text{ 次正确}] \le \left(\frac{3}{4}\right)^m
$$

> **BPP 直观理解**：这证明在随机判定图灵机中，即便单轮查询成功只有一点偏向，只需做多项式次数结合“多数表决”，错误率就被压倒趋近于零。

## Randomized Routing (随机路线规划)

### 问题定义

考虑 $n$ 维超立方体，网络的顶点为 $\{0, 1\}^n$，共 $N = 2^n$ 个。每条边双向，同一条边每个时间只有 **1** 个数据包通过。

令 $\pi$ 是任意排列，目标是在**同一时刻（ $t=0$ ）**，从每个 $i$ **同步出发**发送一个数据包到对应的终点 $\pi(i)$。

整个传输过程是基于同步的离散时间步模型：

- **时间步**：每个数据包每次请求通过一条有向边走一步。
- **拥塞机制**：由于每边单步容量为 1，多个包想走同一条边时，只有 1 个成功，剩下的排队等待，这就产生了**延迟（Delay, $D(i)$）**。

设计路径规划算法的目的是**最小化最大传输时间**。  

这里要求 $i$ 的路径只取决于 $i$ 和 $\pi(i)$，称为 **oblivious 路由**，这是满足局部性的。

**Theorem**: 对于任何确定性 oblivious 的路径规划算法，存在一种排列需要 $\Omega(\sqrt{N/n}) = \Omega(\sqrt{2^n}/n)$ 的时间。

**Theorem**: 存在一种 oblivious **随机路径规划算法**，w.h.p (高概率) 在 $O(n)$ 步停止。

### 随机中转

该思路是“随机中转”，即对每个源节点 $i$，**等概率取样**一个中间节点 $\delta(i)$。传输分为阶段：

1. 从源节点 $i \to$ 中间节点 $\delta(i)$
2. 从中间节点 $\delta(i) \to$ 最终目的地 $\pi(i)$

在两个阶段中，都采用 **bit-fixing**（逐位修复）的策略来决定路径：

在 $n$ 维超立方体中，每个节点都有一个 $n$ 位的二进制编号。网络连边的规则是：**当且仅当两个节点的二进制编号只有 1 位不同时，它们之间才有一条边相连**。

基于这个结构，bit-fixing 寻路方式非常直接：假设当前在节点 $x$，目标是走到节点 $y$。算法从左到右依次比较二者的每一位比特。

一旦发现某一位 $x_k \neq y_k$，就把 $x$ 的第 $k$ 位翻转得到 $x'$，数据包随之沿着连接 $x$ 和 $x'$ 的边前进。由于总共只有 $n$ 位，这种逐位“修齐”的方式保证了任何路径最多只会走 $n$ 步。

### 理论分析与期望求解

因为两个阶段的对称性，不失一般性，我们重点分析第 1 阶段的传输时间。

用 $D(i)$ 表示数据包 $i$ 在路径中**因为拥塞等待而耽误的时间（Delay time）**。

在 $n$ 维超立方体中，起点 $i$ 到 $\delta(i)$ 的基础路径长度最多是 $n$ 步，所以数据包抵达的时间必定等于**实际走过的步数 + 等待的时间**，也就是总时长 $\le n + \max_i D(i)$。

我们接下来的目标是证明：对于任意单个数据包 $i$，严重拥堵的概率极低：

$$ \forall i, \text{Pr}[D(i) > cn] \le e^{-2n} $$

（此处的 $c$ 是后面要通过切尔诺夫界确定的**常数系数**，事实证明 $c = 7/2$ 时满足要求。）

若证明了这点，再根据 **union bound（并集截界）** 推广到全体 $N$ 个数据包：

$$ \text{Pr}[\exists i, D(i) > cn] \le \sum_{i=1}^N \text{Pr}[D(i) > cn] \le 2^n e^{-2n} < 2^{-n} $$

这意味着在 $N \to \infty$ 时，全体数据包的最大等待时间被限制在 $cn$ 以内的概率趋近于 $1$。

#### “锅不能停”定理

用 $P_i$ 表示 $i \to \delta(i)$ 的期望路径所经过的点的集合。定义集合：

$$ S_i = \{ j \neq i \mid P_j \cap P_i \neq \emptyset \} $$

即 $S_i$ 表示所有与数据包 $i$ 的路径 **发生了相交（重叠）** 的其它数据包的集合。

**Claim**: $D(i) \le |S(i)|$

**通俗解释**： 

假设数据包 $i$ 的完整路径为 $P_i$。我们需要解释为什么 $D(i)$ 不会超过这路总共出现过的数据包总数 $|S(i)|$。

这里有两个极其关键的巧妙推导（著名的 Delay Sequence 逻辑）：

1. **路径一旦分开，此生不复相见（只相遇一次）**：这是 **Bit-fixing 规则**的物理性质。因为修位是严格从左到右的！如果车 $i$ 和车 $j$ 在检查第 $k$ 位时分道扬镳了（比如一个翻转了变为 1，一个没动保持 0），此后算法只会去动 $k+1$ 以后的位，**永远不会再回去修改第 $k$ 位**。这意味着它俩的第 $k$ 位从此永远不一样，坐标永远不可能再重合。所以任何包 $j$ 如果驶入 $P_i$，必然是**连续且唯一的一段共享路**。

2. **物理上可能卡你两次，但账本上“背锅侠”变了**：你可能会问：“万一 $j$ 抢了我的道，开去前面后又被车堵了，我追上它，它不就再次堵了我一次吗？”
    确实会！但是，**你是怎么追上 $j$ 的？这说明在追赶的这几秒里，你在“自由通畅”地往前开，而 $j$ 正在前方被卡着！**
    既然 $j$ 被卡着，说明此刻抢占路权的必定是前面一辆新车 $k$。在这个分析模型中，系统只要遇到整体排队停滞，我们都会把“引发延迟的锅”甩给此时此刻长龙里**真正在往前走的排头兵**。
    因为每个人只走一段连续的路，所以 $S_i$ 里的任何一个数据包，终其一生在这条路上能“作为排头兵拔得头筹导致后方延误”的机会是有限的。通过严谨的责任转移， $i$ 受到的每一秒延误，都能完美对应到 $S_i$ 中某个特定成员离开或前进一步消耗的名额中。

**结论**：不管发生了多复杂的连环追尾与超车，你经历的总延迟步数，刚好被那些出现在你前方的总车队大小 $|S_i|$ 严格封顶。

#### 期望计算与 Chernoff Bound 分析

**Lemma**: $\forall i, \text{Pr}[D(i) > cn] \le e^{-2n}$

**证明**： 

我们定义 0-1 指示变量，观察两两是否碰撞：

$$ 
H_{ij} = \begin{cases} 1 & P_i \cap P_j \neq \emptyset \\ 0 & P_i \cap P_j = \emptyset \end{cases} 
$$

由此可以将总延迟的上限转化为求和问题： $D(i) \le \sum_{j \neq i} H_{ij} = |S(i)|$。

由于所有的中间节点 $\delta(\cdot)$ 都是完全随机且独立选取的，这意味着指示变量 $\{H_{ij}\}$ 之间是相互独立的！这完美契合了使用 **Chernoff bound（切尔诺夫界）** 的前提条件。

**第一步：计算期望值 $\mathbb{E}[|S(i)|]$**

这里最容易混淆大 $N$ 和小 $n$。请牢记：大 $N = 2^n$ 是**网络总节点数**，而小 $n$ 是超立方体的**维数（即坐标的比特数）**。

对于超立方体中的每条有向边，它期望会承受多少个数据包呢？

1. **分子（总期望步数）**：网络里总共有 $N$ 个数据包。因为中间节点 $\delta(i)$ 是完全均匀随机挑选的，它和起点 $i$ 的 $n$ 位坐标相比，每一位都有 $1/2$ 的概率不同。因此，每个数据包平均需要翻转（修复） $n/2$ 次比特，也就是**期望走 $n/2$ 步**。所以全局所有数据包走过的总步数期望是 $N \times \frac{n}{2}$ 步。

2. **分母（总有向边数）**：在 $n$ 维超立方体中，每一个节点都有 $n$ 位坐标可以改变，也就是说**每个节点恰好向外连着 $n$ 条有向边**（通向 $n$ 个不同的方向）。因为共有 $N$ 个节点，所以整个网络**有向边的总条数严格等于 $N \times n$**。

基于超立方体绝妙的对称性，**每条有向路平均碰撞期望等于**：

$$ \frac{\text{全部数据包的总期望步数}}{\text{全局有向边总条数}} = \frac{N \times (n/2)}{N \times n} = \frac{1}{2} $$

已知数据包 $i$ 的路径 $P_i$ 长度不会超过 $n$。那么在它的路径上，期望重叠人数为：

$$ \mathbb{E}[|S(i)|] \le (\text{路长上限 } n) \times (\text{单边期望 } 1/2) = \frac{n}{2} $$

**第二步：应用 Chernoff Bound**

根据 Chernoff Bound 公式（上界部分）：

$$ 
\text{Pr}[|S(i)| \ge (1 + \beta)\mu] \le \exp\left(-\frac{\beta^2}{2 + \beta}\mu\right) 
$$

这里 $\mu$ 代表随机变量 $|S(i)|$ 的期望值上限。为了算出一个能容纳最坏情况的极值概率上界（Tail bound），直接代入极值上限 $\mu = \frac{n}{2}$。

取最坏情况 $\mu = \frac{n}{2}$，并令偏差系数 $\beta = 6$。

目标是证明偏离到 $(1+6) \times (n/2) = \frac{7}{2}n$ 时的极小概率，代入公式：

$$ 
\text{Pr}\left[D(i) \ge \frac{7}{2}n\right] \le \text{Pr}\left[|S(i)| \ge \frac{7}{2}n\right] \le \exp\left(-\frac{6^2}{2 + 6} \cdot \frac{n}{2}\right) 
$$

化简得到：

$$ \exp\left(-\frac{36}{8} \cdot \frac{n}{2}\right) = \exp\left(-\frac{9}{4}n\right) $$

显然 $\exp(-\frac{9}{4}n) \le \exp(-2n)$ 成立。

由此得证，当常数 $c = 7/2$ 时（即最大等待时间不超过 $3.5n$ 步），**所有的数据包**高概率能在 $n + \frac{7}{2}n = O(n)$ 步内全部传输完成！这就完成了一个极为精妙的 $O(n)$ 随机算法分析。