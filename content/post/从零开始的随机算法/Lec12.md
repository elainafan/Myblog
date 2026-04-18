---
title: Lecture 12
date: 2026-04-18
encrypt: false
image: "/images/4.jpg"
hidden: true
---
## Power of Two Choice

在传统的随机策略中，最大负载量为 $\Theta\left(\frac{\ln n}{\ln \ln n}\right)$。如果我们在抛球时稍作策略改变，就能让最大负载量呈指数级下降，这就是著名的**Power of two choice**。

### 策略对比

**经典随机策略**：

- $m$ 个球， $n$ 个桶。

- 将球**依次独立均匀**扔到桶里。

- **定理**： $m=n$ 时，最大负载量高概率是 $\Theta\left(\frac{\ln n}{\ln \ln n}\right)$。

**选择两个桶策略 (Power of two choice)**：

- $m$ 个球， $n$ 个桶。

- **每次扔球时选两个桶，把球放到球少的桶里**（如果有平局则任选其一均可）。

- **定理**： $m=n$ 时，最大负载量高概率不超过 $\frac{\ln \ln n}{\ln 2} + \Theta(1)$。

这种策略通过常数次的额外探查，将最大负载的高概率界从对数级别 $\Theta(\frac{\ln n}{\ln \ln n})$ 降低到了双重对数级别 $O(\ln \ln n)$。

### 分析目标与核心思路

根据定理，要证明最大负载量高概率不超过目标界限，等价于证明其对立事件（即存在桶的负载量超过界限）的概率趋向于 0。

1. **变量定义**：

   定义随机变量 $B_i$：

$$
B_i = \text{负载量 } \ge i \text{ 的桶的数量}
$$

2. **分析目标 (Goal)**：证明在界限 $\frac{\ln \ln n}{\ln 2} + \Theta(1)$ 处存在桶的概率趋向于 0：

$$
\Pr\left[B_{\frac{\ln \ln n}{\ln 2} + \Theta(1)} \ge 1\right] = O\left(\frac{(\ln n)^2}{n}\right)
$$

### 归纳递推

为了计算 $B_i$ 的变化，我们使用**数学归纳法 (Induction)**。

设置一个边界序列 $\beta_1, \beta_2, \cdots$，归纳目标为证明：在**高概率**下，对于所有的 $i$，均满足 $B_i < \beta_i$。

**随机占优与二项分布包络：**

- 在采用选择两个桶策略时，若要使某球落入后形成高度 $\ge i+1$ 的桶，该球在抛掷时探查的两个桶的高度均须已经 $\ge i$。

- 假设条件 $B_i \le \beta_i$ 成立（即高度 $\ge i$ 的桶数受控于 $\beta_i$）。每次独立、有放回地选取两个桶，它们高度均 $\ge i$ 的概率上限为：

$$
p = \left(\frac{\beta_i}{n}\right)^2
$$

- 共计投掷 $n$ 个球。考察所有使得目标桶高度达到 $\ge i+1$ 的球，每一个这类球落入目标桶的必要条件是其探查的两个桶均 $\ge i$。在 $B_i \le \beta_i$ 的条件下，发生此事件的球的总数可被二项分布 $\text{Binomial}(n, p)$ 随机占优 (Stochastically Dominated)。

- 由于高度 $\ge i+1$ 的桶数 $B_{i+1}$ 必定小于等于使桶高达到 $i+1$ 时的关键球总数，因此可得放缩：

$$
B_{i+1} \le_1 \text{Binomial}\left(n, \left(\frac{\beta_i}{n}\right)^2\right)
$$

为了运用 Chernoff 界控制尾部概率，设定递推公式：

$$
\beta_{i+1} = \frac{e\beta_i^2}{n}
$$

**基准情形：**

我们不从第一层开始计算界限，而是从一个常数层开始（比如 $i=6$），此时设定：

$$
\beta_6 = \frac{n}{2e}, \quad B_6 \le \beta_6
$$

### 证明归纳

为了证明总目标，将推理划分为两部分：长序递推阶段的引理 1，以及终局常数层的引理 2。

### 引理 1 分析

在归纳过程中， $\beta_i$ 随层数 $i$ 的增加呈现平方级衰减。在应用 Chernoff 界时，指数项界限形式为 $e^{-\mu}$，其中 $\mu = n \cdot (\beta_i/n)^2 = \frac{\beta_i^2}{n}$。要使单层失效概率满足 $\le \frac{1}{n^2}$，即具备足够小的渐近上界以抵消无穷级数求和，应要求期望部分满足 $\mu \ge 2\ln n$ 成立。这构成了引理 1 的核心生效条件。

**引理 1**：对于所有 $i > 6$，在满足 $\frac{\beta_i^2}{n} \ge 2\ln n$ 的前提下，有：

$$
\Pr[B_i > \beta_i] \le \frac{i}{n^2}
$$

### 引理 1 证明

为计算 $B_{i+1}$ 超过阈值 $\beta_{i+1}$ 的概率，基于前提事件 $B_i$ 的状态进行全概率展开并放缩：

<div>
$$
\begin{aligned}
\Pr[B_{i+1} > \beta_{i+1}] &= \Pr[B_{i+1} > \beta_{i+1} \mid B_i \le \beta_i] \Pr[B_i \le \beta_i] + \Pr[B_{i+1} > \beta_{i+1} \mid B_i > \beta_i] \Pr[B_i > \beta_i] \\\\
&\le \Pr[B_{i+1} > \beta_{i+1} \mid B_i \le \beta_i] + \Pr[B_i > \beta_i]
\end{aligned}
$$
</div>

对该不等式的第一项进行分析（即条件限制 $B_i \le \beta_i$ 下层级的递进概率）：

引入示性随机变量 $I_k$ 表示第 $k$ 个投入的球处于高度 $\ge i+1$。“两桶选择”规则下，单层递增要求其选取的两个目标桶的高度皆已 $\ge i$；在给定当前桶数限制界限 $\beta_i$ 时，此条件事件的概率上限应为 $p \le (\beta_i/n)^2$。

考虑到经过全部 $n$ 次具有放回投球过程，总计高度达到 $i+1$ 刻度的桶的总数目必定不大于具备达成该性质高度投出球的总合迹，即满足 $B_{i+1} \le \sum_{k=1}^n I_k$。

基于每次抛球受制于单次独立上限试验 $p$，桶数目上限随机变量序列被该上界独立抛掷序列形成的二项分布 $X \sim \text{Binomial}(n, (\beta_i/n)^2)$ 随机占优包络。

推演条件概率的首项可表述为：

$$
\Pr[B_{i+1} > \beta_{i+1} \mid B_i \le \beta_i] \le \Pr\left[\text{Binomial}\left(n, \left(\frac{\beta_i}{n}\right)^2\right) > \beta_{i+1}\right]
$$

代入给定的递推关系式 $\beta_{i+1} = \frac{e\beta_i^2}{n}$：

$$
\Pr\left[\text{Binomial}\left(n, \left(\frac{\beta_i}{n}\right)^2\right) > \frac{e\beta_i^2}{n}\right]
$$

按照 Chernoff 界的偏度标准变形（对于 $X \sim \text{Binomial}(n, p)$，取界限为数学期望 $\mu$ 的 $e$ 倍，具约束 $\Pr[X > e\mu] \le e^{-\mu}$）。在此定义下，设定变量期望 $\mu = n \cdot (\beta_i/n)^2 = \frac{\beta_i^2}{n}$，得对应放缩式：

$$
\le e^{-\frac{\beta_i^2}{n}}
$$

代入引理给定量要求 $\frac{\beta_i^2}{n} \ge 2\ln n$ 约束后收缩：

$$
e^{-\frac{\beta_i^2}{n}} \le e^{-2\ln n} = \frac{1}{n^2}
$$

最后，回代整合最初全概率分解所提尾项 $\Pr[B_i > \beta_i]$；依递推假定，对多步级数每次引入误差 $O(1/n^2)$。加总累计完美证实本层的失效限度能被界 $\Pr[B_{i+1} > \beta_{i+1}] \le O(i/n^2)$ 严格覆盖。

### 引理 2：常数层分析

由于 $\beta_{i+1} = \frac{e\beta_i^2}{n}$ 是平方递减序列，经过 $O(\log \log n)$ 步数之后，引理 1 的前提条件将无法继续维持。

设 $i^{\ast}$ 为满足条件 $\frac{\beta_i^2}{n} < 2\ln n$ 的首个最小层数。

不难解出此时 $i^{\ast} = \frac{\ln \ln n}{\ln 2} + O(1)$。

接下来对 $i^{\ast} + 1$ 与 $i^{\ast} + 2$ 层的最大负载概率分别进行放缩以证明全集界限。

#### Claim 1

由于我们处于 $i^{\ast}$ 会打破前提条件的状态，可知 $\beta_{i^{\ast}} \le \sqrt{2n \ln n}$。

利用全概率公式拆解第 $i^{\ast}+1$ 层的突破概率：

$$
\Pr[B_{i^{\ast}+1} \ge 6 \ln n] \le \Pr[B_{i^{\ast}+1} \ge 6 \ln n, B_{i^{\ast}} \le \sqrt{2n \ln n}] + \Pr[B_{i^{\ast}} > \sqrt{2n \ln n}]
$$

1. **后面一项 $\Pr[B_{i^{\ast}} > \sqrt{2n \ln n}]$**：

   根据 $i^{\ast}$ 的定义， $i^{\ast}$ 是首个满足 $\frac{\beta_i^2}{n} < 2\ln n$ 的层级。因此在其上一层 $i^{\ast}-1$，条件 $\frac{\beta_{i^{\ast}-1}^2}{n} \ge 2\ln n$ 仍然严格成立。

   这意味着我们可以对 $i^{\ast}-1$ 层到 $i^{\ast}$ 层的推导继续使用引理 1 的结论，即 $\Pr[B_{i^{\ast}} > \beta_{i^{\ast}}] \le \frac{i^{\ast}}{n^2}$。

   由于定义中 $\beta_{i^{\ast}} \le \sqrt{2n \ln n}$，故 $\Pr[B_{i^{\ast}} > \sqrt{2n \ln n}] \le \Pr[B_{i^{\ast}} > \beta_{i^{\ast}}] \le \frac{1}{n}$。

2. **前面一项 $\Pr[B_{i^{\ast}+1} \ge 6 \ln n \mid B_{i^{\ast}} \le \sqrt{2n \ln n}]$**：

   在已知条件 $B_{i^{\ast}} \le \sqrt{2n \ln n}$ 成立的前提下，高度大于等于 $i^{\ast}$ 的桶的数量至多为 $\sqrt{2n \ln n}$。

   对于投掷的任意一个新球，只有当它两次独立随机选择的桶的高度均已经 $\ge i^{\ast}$ 时，才可能在其落入后产生高度为 $i^{\ast}+1$ 的桶。

   该单次投掷满足条件的概率为 $p \le \left(\frac{\sqrt{2n \ln n}}{n}\right)^2 = \frac{2\ln n}{n}$。

   利用随机占优 (Stochastic Dominance)，在 $n$ 次投掷中，落入高度 $\ge i^{\ast}$ 桶中的总球数受控于二项分布 $X \sim \text{Bin}(n, p)$。

   该二项分布的期望为 $\mu = n \cdot \frac{2\ln n}{n} = 2\ln n$。

   根据 Chernoff 界，求偏离期望至 $6\ln n = 3\mu$ 的概率（取 $\delta=2$）：

$$
\Pr[X \ge 3\mu] \le \left( \frac{e^2}{3^3} \right)^\mu < 2^{-2\ln n} = \frac{1}{n^2}
$$

   因此， $\Pr[B_{i^{\ast}+1} \ge 6 \ln n \mid B_{i^{\ast}} \le \sqrt{2n \ln n}] \le \frac{1}{n^2} \le \frac{1}{n}$ 。

综合两项可得：

$$
\Pr[B_{i^{\ast}+1} \ge 6 \ln n] \le \frac{1}{n} + \frac{1}{n^2} = O\left(\frac{1}{n}\right)
$$

即 Claim 1 得证。

#### Claim 2

类似于 Claim 1，我们分析 $i^{\ast}+2$ 层存在桶（即最大负载达到 $i^{\ast}+2$）的概率。对事件进行条件分解：

$$
\Pr[B_{i^{\ast}+2} \ge 1] \le \Pr[B_{i^{\ast}+2} \ge 1 \mid B_{i^{\ast}+1} \le 6 \ln n] + \Pr[B_{i^{\ast}+1} > 6 \ln n]
$$

1. **后面一项 $\Pr[B_{i^{\ast}+1} > 6 \ln n]$**：

   直接由 Claim 1 的结论可知，该概率常数界趋近于 $O(1/n)$。

2. **前面一项 $\Pr[B_{i^{\ast}+2} \ge 1 \mid B_{i^{\ast}+1} \le 6 \ln n]$**：

   在已知条件 $B_{i^{\ast}+1} \le 6 \ln n$ 成立的前提下，高度大于等于 $i^{\ast}+1$ 的桶的数量至多为 $6 \ln n$。

   新投掷的任何一个球，只有当其两次独立随机选择的桶的高度均已经 $\ge i^{\ast}+1$ 时，才可能在其落入后产生高度为 $i^{\ast}+2$ 的桶。

   该单次投掷满足条件的概率为 $p \le \left(\frac{6\ln n}{n}\right)^2 = \frac{36\ln^2 n}{n^2}$。

   利用随机占优 (Stochastic Dominance)，在 $n$ 次投掷中，落入高度 $\ge i^{\ast}+1$ 桶中的总球数受控于二项分布 $Y \sim \text{Bin}(n, p)$。

   我们要计算的是产生至少 1 个这样的桶的概率，即 $\Pr[Y \ge 1]$。

   该二项分布的期望为 $\mu = n \cdot \frac{36\ln^2 n}{n^2} = \frac{36\ln^2 n}{n}$。

   利用 Union Bound（或马尔可夫不等式 $\Pr[Y \ge 1] \le \mathbb{E}[Y]$），可得：

$$
\Pr[Y \ge 1] \le \mathbb{E}[Y] = \frac{36\ln^2 n}{n} = O\left(\frac{\log^2 n}{n}\right)
$$

综合两项可得：

$$
\Pr[B_{i^{\ast}+2} \ge 1] \le O\left(\frac{\log^2 n}{n}\right) + O\left(\frac{1}{n}\right) = O\left(\frac{\log^2 n}{n}\right)
$$

这证明了产生高度为 $i^{\ast}+2$ 的桶的概率趋于 0。从而以高概率保证了最大负载 $O(\log \log n)$。

#### 总结与推广

整合以上多步归纳的上限界定理：

- **引理 1 (前置长序列期)** $i \le i^{\ast}$ 时（即达到 $\frac{\ln \ln n}{\ln 2}$ ），由于受二项分布平滑包络影响，高度大于界限值的桶随序列平方级急剧减少。

- **引理 2 (临界末端层)** 越过层数阈值 $i^{\ast}$ 之后，在接下来的仅数个常数层（引理证明中体现为 $i^{\ast}+2$ 的高度）即可产生极趋于零的崩溃概率。

两者相结合，由此得出对经典“球与桶”随机模型的分析，当将随机选取策略切换为“选择两个桶”时，以极高概率能够将最大负载高度界抑制于其上确界： $i^{\ast} + 2 = \frac{\ln \ln n}{\ln 2} + O(1)$ 。

**补充推断与推广**：

- **紧下确界性质**：经过严谨的反向证明论证，其负载期望在 w.h.p（以高概率趋近于1的概率性质）条件下取得同样是 $\Omega(\ln \ln n)$。推导获得的界限属于紧密确定的最佳包络边界（Tight Bound）。

- **推广至多桶模型 (Power of $d$ Choices)**：当一次探查能够选择从原来的 $2$ 桶扩展为投向任意独立选出的 $d$ 桶时，每次错误选取对应概率受控降级为 $(\frac{\beta_i}{n})^d$ ；依同等归纳策略处理递归过程后，最大负载的上限界将快速收敛至 $\frac{\ln \ln n}{\ln d} + O(1)$。