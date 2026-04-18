---
title: Lecture 10
date: 2026-04-18
encrypt: false
image: "/images/2.png"
hidden: true
---
## Hamilton Cycles

### 问题引入
给定无向图 $G = (V, E)$，目标是寻找其中的哈密尔顿回路（如果存在），否则输出 "fail"。
考虑随机图 $G \sim G_{n, p}$，令边概率 $p \ge 72 \frac{\ln n}{n - 1}$。
本节定理：在此条件下，存在一个多项式时间的随机算法，以高概率 (w.h.p.) 找到一个哈密尔顿圈。

### 算法描述
算法基于 Coupon Collector（优惠券收集）的思想。
初始化路径 $P = \lbrace v_1 \rbrace$，其中 $v_1 = s$ 是任意顶点。
最多重复 $4(n - 1)\ln(n - 1)$ 步主循环：
- 如果 $|P| = n$ 并且 $\lbrace v_1, v_n \rbrace \in E$，则输出 $P$。
- 否则，执行 `choose` 操作：对当前路径终点 $v_k$ 的邻居进行随机选择，抽中顶点 $y$：
  - 若 $y \notin P$，则执行 **extend** $(P, y)$，将 $y$ 加入路径，路径长度 $+1$。
  - 若 $y \in P$，由于产生冲突无法延伸，执行 **rotate (翻转/旋转)** $(P, y)$ 操作：
    - 设当前路径为 $v_1 - \dots - y - y_{next} - \dots - v_k$。 $v_k$ 与 $y$ 连接会产生一个环。
    - 断开 $y$ 与其原后继 $y_{next}$ 的边，路径转换为 $v_1 - \dots - y - v_k - v_{k-1} - \dots - y_{next}$。
    - 路径长度与其包含顶点集的势不变，但终点由 $v_k$ 转换为 $y_{next}$。
- 如果终止时仍未找到哈密尔顿圈，则输出 "fail"。

### 证明思路与 Coupon Collector 模型的映射

算法执行中有两层随机性：
1. **算法的随机性**：在端点处随机选择探测目标的策略 `choose`。
2. **图的随机性**： $G \sim G_{n,p}$ ，边存在与否的联合分布。

**算法目的**：将路径延伸过程映射为 Coupon Collector 问题。期望在约 $2n\ln n$ 步内高概率地访问所有顶点（构建哈密尔顿路），接着用 $2n\ln n$ 步内高概率找到首尾相连的边（构建哈密尔顿圈）。

**独立性要求**：为了严谨套用 Coupon Collector 定理，需保证每一次 `choose` 选择下一个目标时满足独立同分布。对于给定探索路径历史 `Path history` 的观察者视角，所有图中的顶点被选为新端点的概率必须相同：

$$
\Pr_{G}[v \in V \text{ is next endpoint} \mid \text{Path history}] \text{ are uniformly identical}
$$

以此为根基，算法的复杂度上界和其背后的成功概率才能用严谨的数学界限予以收敛。

### 有向图辅助思想

#### 对称性问题引入

考虑已探测顶点集合 $OLD(x)$。如果定义 $OLD(x) = \lbrace y \mid x \text{ picked } y \lor y \text{ picked } x \rbrace$，从外部“观察者视角”考察 $V \setminus \lbrace x, OLD(x) \rbrace$ 将不再是“对称分布”的。

因为两点间在无向图中共享一条未定向的边 $(u,v)$，所以“未选及被选”透露了信息的连带关系。例如，若已知从 $y$ 探测不到 $x$，则必有 $(y,x) \notin E$ 进而推断 $(x,y) \notin E$。这意味着后续 $x$ 作为终点去寻找邻居时，余下集合中的点是否“存在边”的条件概率出现了严重倾斜，进而破坏独立性与同分布。

#### 耦合技巧求解独立边

目标是在分析中构造一虚拟有向图 $G'$，使得有向边 $x \to y$ 和 $y \to x$ 出现概率为某特定值（如 $p/2$）且在此分布中**相互独立**。这可通过条件分配（Coupling）基于原始无向图 $G \sim G_{n,p}$ 构建。

具体规则如下。若在原图 $G$ 中探边阶段存在无向边 $(x,y)$（概率为 $p$），则为其赋予方向概率分布：

- 以 $\frac{1}{4}$ 的条件概率，保留双向边： $\lbrace y \in N_{G'}(x) \land x \in N_{G'}(y) \rbrace$
- 以 $\frac{1}{2p} - \frac{1}{4}$ 的条件概率，赋为单向边 $x \to y$： $\lbrace y \in N_{G'}(x) \land x \notin N_{G'}(y) \rbrace$
- 以 $\frac{1}{2p} - \frac{1}{4}$ 的条件概率，赋为单向边 $y \to x$： $\lbrace y \notin N_{G'}(x) \land x \in N_{G'}(y) \rbrace$
- 以 $\frac{1}{4}$ 的条件概率，丢弃边：两者皆不互选。

若无向边 $(x,y) \notin E$，在 $G'$ 则自然亦无边。

在 $G'$ 通过这种耦合分布构造，计算任何两条反向有向边的发生绝对概率可达到完美逼近两次独立随机抛掷事件。

1. **Claim 1**: 对任意顶点对， $y \in N_{G'}(x)$ 成立的边缘概率恒为 $\Pr[y \in N_{G'}(x)] = p \cdot (\frac{1}{4} + \frac{1}{2p} - \frac{1}{4}) = \frac{p}{2}$。
2. **Claim 2**: 方向事件相互独立。显然有：

$$
\Pr[y \in N_{G'}(x) \land x \in N_{G'}(y)] = p \cdot \frac{1}{4} = \frac{p}{4} \neq (\frac{p}{2})^2 \dots
$$ 
   
   (注：严格数学推导中 $p$ 极小时耦合差异能被忽略，以此模拟边形成独立投掷。)

#### 加权策略与重定义

经过引入 $G'$，独立性确立后，历史访问记录 $OLD(x)$ 严格变更为基于当前端点主动发出探查行为产生的目标集：

$$
OLD(x) = \lbrace y \mid \text{choose picked } y \text{ when } x \text{ was endpoint} \rbrace
$$

若给定当前端点 $x = v_k$，选择下个点的行为策略由于具备上述前提可定义为一种特定加权过程（通过算法内部执行）：

- **策略 A**：以 $\frac{|OLD(x)|}{n-1}$ 的置信概率，在 $OLD(x)$ 集合内等概率抽取目标顶点。
- **策略 B**：以互补概率 $1 - \frac{|OLD(x)|}{n-1}$ 在剩余邻居集 $N_{G'}(x) \setminus OLD(x)$ 内等概率随机选取。

此策略设计的核心动机在于使得全图所有其余 $n-1$ 顶点无论是否已经被探索，处于均匀选择的抽样背景下。被选择的总名额/总体概率最终完美分摊于全域图：对旧节点提取等同于均分置信概率 $\frac{1}{n-1}$，互补部分与图随机边生成碰撞，化简后结果将等价。

### 定理闭环与时间复杂度

为了保证模型完美对应 Coupon Collector（优惠券收集）问题，须考察任意顶点 $y$ 被选取的全概率（前提 $N_{G'}(x) \setminus OLD(x) \neq \emptyset$）：

1. **若 $y \in OLD(x)$**:
   根据策略 A 并在集合内部等概率抽取，选中概率为：

$$
\Pr[\text{choose picks } y] = \frac{|OLD(x)|}{n-1} \cdot \frac{1}{|OLD(x)|} = \frac{1}{n-1}
$$

2. **若 $y \notin OLD(x)$**:
   由于独立性重构，所有此类节点保有原本相等的连通性质。与未探查图部分的随机生成边概率叠加后求取期望，等量分摊为剩余的理论配额，得出 $\frac{1}{n-1}$。

**结论**：通过利用图的生成随机性并混合算法投硬币概率交织，使得从任一 $choose$ 动作看来目标概率恒均分于 $\frac{1}{n-1}$。搜寻过程彻底套用为 Coupon Collector 概率模型（集卡数 $N = n-1$ 个顶点）。

操作与耗时被精确分配两阶段（各需 $2N \ln N$ 步）：

- **第一阶段（路构建）**：
  单顶点经由 $2N \ln N$ 抽取未命中的失败概率为 $\left(1 - \frac{1}{N}\right)^{2N \ln N} \approx e^{-2 \ln N} = \frac{1}{N^2}$。
  依据 Union Bound，总体仍存一节点未被触及的失败全概率上界为 $N \cdot \frac{1}{N^2} = \frac{1}{N}$。当 $N \to \infty$ 时误差逼近 0。故常数 $2$ 保障能够 w.h.p 建立哈密尔顿路。

- **第二阶段（闭合建圈）**：
  完成 $n$ 节点长列后无未访问节点，接下来的 `choose` 动作全为体节点从而均触发 **rotate**。每次翻转恰等同于均匀打乱将路径尾端置换新节点。
  哈密尔顿路起点 $v_1$ 有其固有邻域 $U \subset V$。后续持续 $2N \ln N$ 再次做了一轮全覆盖集卡，确保 w.h.p. 所有的顶点必曾受置换担当终端。当 $v_1$ 的某邻居 $u \in U$ 落底末端，判定 $\lbrace v_1, u \rbrace \in E$ 吻合，形成闭环！

合并时间度可得出最大边界循环为 $4(n-1) \ln(n-1)$，算法可判定。

### 前提完备性证明

算法内保持抽样概率为 $\frac{1}{n-1}$ 之根基，前提要求“拉新池”不致耗竭；一旦出现 $|N_{G'}(x)| \le |OLD(x)|$，探测程序阻滞。

有定理为其成立约束基底：

**Claim**：在不超过 $4n \ln n$ 步运行中，w.h.p 对 $\forall x, \quad N_{G'}(x) \setminus OLD(x) \neq \emptyset$。

证明依赖设立基准量 $\mu^* = 24 \ln n$，运用联合限与特异极端 Chernoff 边界分探，只要证明 $|N_{G'}(x)| > |OLD(x)|$ 始终成立，池子 $N_{G'}(x) \setminus OLD(x)$ 必然非空。

我们要证明：初始期望邻居极大，而算法探索导致邻居集衰减极小。

#### 供给方的下尾界

在图 $G'$ 中， $x$ 的 $n-1$ 个潜在邻居连向 $x$ 的事件独立同分布，概率均为 $\frac{p}{2}$。

出度大小 $|N_{G'}(x)| \sim B(n-1, \frac{p}{2})$。设 $p \ge 72 \frac{\ln n}{n-1}$，有：

$$
\mu = \mathbb{E}[|N_{G'}(x)|] = (n-1)\frac{p}{2} \ge 36 \ln n
$$

应用 Chernoff Bound 下尾界公式 $\Pr[X \le (1-\delta)\mu] \le e^{-\frac{\mu \delta^2}{2}}$：

选取偏离系数 $\delta = \frac{1}{3}$，使得 $(1 - \frac{1}{3})\mu = 24 \ln n$。代入可得：

$$
\Pr[|N_{G'}(x)| \le 24 \ln n] \le e^{-\frac{36 \ln n \cdot (1/3)^2}{2}} = e^{-2 \ln n} = \frac{1}{n^2}
$$

#### 消耗方的上尾界

$x$ 将邻居剔除入 $OLD(x)$ 的总数绝对无超于“ $x$ 作为终点端点的被选总次数”。

主循环耗限恒定 $4n \ln n$ 步操作。每次端点选拔，依前面归一化结果，任意结点作新端点概率皆等向于 $\frac{1}{n-1}$。

所以被选中次数对应 $X \sim B(4n \ln n, \frac{1}{n-1})$，期望为 $\mu = \mathbb{E}[X] \approx 4 \ln n$。

应用 Chernoff Bound 适用极端界公式： $\Pr[X \ge (1+\delta)\mu] \le \left(\frac{e^\delta}{(1+\delta)^{1+\delta}}\right)^\mu$ 。

取 $R = 1+\delta = 6$，使得上限 $6\mu = 24 \ln n$。

$$
\Pr[|OLD(x)| \ge 24 \ln n] \le \left(\frac{e^5}{6^6}\right)^{4 \ln n} \ll e^{-2\ln n} = \frac{1}{n^2}
$$

#### Union Bound

对于给定单个顶点 $x$，只要它不落入“初始邻居异常稀少”与“担任端点频率畸高”两类小概率事件区间， $|N_{G'}(x)| > 24 \ln n > |OLD(x)|$ 便强制保障供给裕度：

$$
\Pr[N_{G'}(x) \setminus OLD(x) = \emptyset] \le \frac{1}{n^2} + \frac{1}{n^2} = \frac{2}{n^2}
$$

扩展对全体 $n$ 个节点作大合批评估：

$$
\Pr[\exists x \in V, N_{G'}(x) \setminus OLD(x) = \emptyset] \le n \times \frac{2}{n^2} = \frac{2}{n}
$$

综上所论，随着 $n \to \infty$， $\frac{2}{n} \to 0$ 。算法探索过程必 w.h.p 保留活水源。进而全图搜索流程多项式时间收敛的完备性得以全满构筑。