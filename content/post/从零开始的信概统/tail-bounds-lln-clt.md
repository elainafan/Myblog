---
title: 尾不等式、大数定律和中心极限定理
date: 2026-01-02
categories:
    - 数学
slug: 尾不等式、大数定律和中心极限定理
hidden: true
seriesOrder: 6
---

Markov 和 Chebyshev 在较弱条件下给出尾界，Chernoff 和 Hoeffding 则利用独立性得到指数衰减。大数定律描述样本均值的收敛，中心极限定理进一步刻画标准化后的分布。

## 尾不等式的目标

在 $n$ 重伯努利试验中，令 $n_A$ 为事件 $A$ 发生的次数，频率为

$$
f_n(A)=\frac{n_A}{n}.
$$

若 $P(A)=p$ ，则 $n_A\sim B(n,p)$ ，且 $E(n_A)=np$ 。我们关心两类问题

- 尾不等式，给出 $P(X\geq k)$ 的上界。
- 集中不等式，给出 $P(|X-E(X)|\geq k)$ 的上界。

例如

$$
P(|f_n(A)-p|\geq \epsilon)=P(|n_A-E(n_A)|\geq n\epsilon).
$$

若能证明该概率趋于 $0$ ，就得到频率收敛到概率的大数定律。

## Markov 与 Chebyshev

Markov 和 Chebyshev 所需条件较弱，相应的上界通常也比较宽松。

Markov 不等式，若 $X\geq 0$ ，则对 $a \gt 0$ 有

$$
P(X\geq aE(X))\leq \frac{1}{a}.
$$

Chebyshev 不等式

$$
P(|X-E(X)|\geq c\sigma(X))\leq \frac{1}{c^2}.
$$

对 $n_A\sim B(n,p)$ ，有 $\mathrm{Var}(n_A)=np(1-p)$ ，因此

$$
P(|n_A-E(n_A)|\geq n\epsilon)\leq \frac{p(1-p)}{n\epsilon^2}.
$$

这个上界已经可以推出

$$
\lim_{n\to+\infty}P(|f_n(A)-p| \lt \epsilon)=1.
$$

Chebyshev 只使用二阶矩，对 Bernoulli 试验的全部独立性没有充分利用。

## 高阶矩方法

二阶矩得到的界较松时，可以对更高的偶数阶中心矩使用 Markov 不等式。

给定随机变量 $X$ ， $E(X^k)$ 称为 $k$ 阶原点矩， $E((X-E(X))^k)$ 称为 $k$ 阶中心矩。

若 $X\sim B(n,p)$ ，可以通过矩生成函数计算四阶中心矩。令

$$
M_X(t)=E(e^{tX}).
$$

则

$$
M_X(t)=(1-p+pe^t)^n.
$$

令 $Y=X-E(X)$ ，则

$$
M_Y(t)=M_X(t)e^{-tE(X)}.
$$

于是

$$
E(Y^4)=M_Y^{(4)}(0)
=np(1-p)^4+n(1-p)p^4+3n(n-1)p^2(1-p)^2.
$$

当 $p=\frac{1}{2}$ 时

$$
E((X-E(X))^4)=\frac{n(3n-2)}{16}=O(n^2).
$$

由 Markov 不等式

$$
P(|X-E(X)|\geq n\epsilon)
\leq
\frac{E((X-E(X))^4)}{n^4\epsilon^4}
=O\left(\frac{1}{n^2\epsilon^4}\right).
$$

四阶矩把衰减从 $O(1/n)$ 提高到 $O(1/n^2)$ ，但仍未得到指数尾界。

## Chernoff Bound

Chernoff Bound 对指数变量 $e^{tX}$ 使用 Markov 不等式。指数函数放大尾部，只要矩生成函数可控，就能得到比有限阶矩更强的估计。

若 $t \gt 0$ ，则

$$
P(X\geq k)\leq e^{-tk}M_X(t).
$$

若 $t \lt 0$ ，则

$$
P(X\leq k)\leq e^{-tk}M_X(t).
$$

对 $X\sim B(n,p)$ ，有

$$
M_X(t)=(1-p+pe^t)^n.
$$

结合 Hoeffding 引理可以得到二项分布的常用形式

$$
P(X-E(X)\geq n\epsilon)\leq e^{-2n\epsilon^2},
$$

以及

$$
P(X-E(X)\leq -n\epsilon)\leq e^{-2n\epsilon^2}.
$$

因此

$$
P(|X-E(X)|\geq n\epsilon)\leq 2e^{-2n\epsilon^2}.
$$

## Hoeffding 引理与 Chernoff-Hoeffding

Hoeffding 引理控制有界随机变量的中心矩生成函数，与 Chernoff Bound 结合后可得独立有界随机变量的集中不等式。

Hoeffding 引理，若 $a\leq X\leq b$ ，则

$$
E(e^{t(X-E(X))})\leq \exp\left(\frac{t^2(b-a)^2}{8}\right).
$$

若 $X=\sum_{i=1}^{n}X_i$ ，其中 $X_i$ 相互独立且 $a\leq X_i\leq b$ ，则

$$
P(X\geq E(X)+k)\leq \exp\left(-\frac{2k^2}{n(b-a)^2}\right),
$$

以及

$$
P(X\leq E(X)-k)\leq \exp\left(-\frac{2k^2}{n(b-a)^2}\right).
$$

证明过程分为四步

1. 对 $X-E(X)$ 使用 Chernoff bound。
2. 利用独立性把矩生成函数拆成乘积。
3. 对每一项使用 Hoeffding 引理。
4. 对 $t$ 求最优值。

## 大数定律

大数定律描述样本平均在依概率意义下的稳定性，并不等同于每条样本路径都收敛。

### 伯努利大数定律

在 $n$ 重伯努利试验中，对任意 $\epsilon \gt 0$ ，有

$$
\lim_{n\to+\infty}P\left(\left|\frac{n_A}{n}-p\right| \lt \epsilon\right)=1.
$$

### Markov 大数定律

若随机变量序列 $X_1,X_2,\ldots$ 满足

$$
\frac{1}{n^2}\mathrm{Var}\left(\sum_{i=1}^{n}X_i\right)\to 0,
$$

则

$$
\frac{1}{n}\sum_{i=1}^{n}X_i-\frac{1}{n}\sum_{i=1}^{n}E(X_i)\xrightarrow{P}0.
$$

由 Chebyshev 不等式即可得到该结论。

例如，若 $X_i$ 同分布，每个 $X_i$ 只可能与 $X_{i-1}$ 和 $X_{i+1}$ 相关，其余分量不相关，则

$$
\mathrm{Var}\left(\sum_{i=1}^{n}X_i\right)=O(n),
$$

因此满足 Markov 大数定律。

### Khinchin 大数定律

若 $X_1,X_2,\ldots$ 独立同分布，且 $E(X_i)=\mu$ 存在，则

$$
\frac{1}{n}\sum_{i=1}^{n}X_i\xrightarrow{P}\mu.
$$

Khinchin 大数定律只要求期望存在，不要求方差有限。

## 随机变量序列的收敛

依概率收敛控制随机变量本身偏离极限的概率，依分布收敛只要求分布函数在连续点处收敛。

### 依概率收敛

若对任意 $\epsilon \gt 0$ 有

$$
\lim_{n\to+\infty}P(|Y_n-Y|\geq \epsilon)=0,
$$

则称 $Y_n$ 依概率收敛到 $Y$ ，记作

$$
Y_n\xrightarrow{P}Y.
$$

### 依分布收敛

若对 $F_Y$ 的任意连续点 $x$ ，都有

$$
\lim_{n\to+\infty}F_{Y_n}(x)=F_Y(x),
$$

则称 $Y_n$ 依分布收敛到 $Y$ ，记作

$$
Y_n\xrightarrow{d}Y.
$$

依概率收敛推出依分布收敛。若极限 $Y$ 是常数，则依概率收敛与依分布收敛等价。

## 特征函数

特征函数对任意随机变量都存在，并且把独立随机变量之和转化为特征函数的乘积。

随机变量 $X$ 的特征函数定义为

$$
\phi_X(t)=E(e^{itX}).
$$

与矩生成函数不同，特征函数对任意随机变量都存在，因为 $|e^{itX}|=1$ 。

常用性质

$$
\phi_{aX+b}(t)=e^{itb}\phi_X(at).
$$

若 $X_1,\ldots,X_n$ 相互独立，且 $X=\sum_iX_i$ ，则

$$
\phi_X(t)=\prod_{i=1}^{n}\phi_{X_i}(t).
$$

若矩存在，则

$$
\phi_X^{(k)}(0)=i^kE(X^k).
$$

特征函数唯一决定分布，并且有连续性定理

$$
X_n\xrightarrow{d}X
\quad\Longleftrightarrow\quad
\phi_{X_n}(t)\to \phi_X(t)
$$

对任意 $t$ 成立，且极限函数在 $0$ 处连续。

常见特征函数

$$
X\sim N(\mu,\sigma^2)\quad\Rightarrow\quad
\phi_X(t)=e^{i\mu t-\sigma^2t^2/2}.
$$

$$
X\sim \pi(\lambda)\quad\Rightarrow\quad
\phi_X(t)=e^{\lambda(e^{it}-1)}.
$$

$$
X\sim B(n,p)\quad\Rightarrow\quad
\phi_X(t)=(1-p+pe^{it})^n.
$$

标准柯西分布的特征函数为

$$
\phi_X(t)=e^{-|t|}.
$$

因此独立同分布柯西随机变量的平均值仍服从同一个柯西分布，这说明 Khinchin 大数定律不能去掉期望存在的条件。

## 中心极限定理

大数定律给出样本均值的极限，中心极限定理则描述均值附近波动的渐近分布。

设 $X_1,X_2,\ldots$ 独立同分布，且

$$
E(X_i)=\mu,\qquad \mathrm{Var}(X_i)=\sigma^2.
$$

令

$$
S_n=\sum_{i=1}^{n}X_i.
$$

Lindeberg-Levy 中心极限定理说明

$$
\frac{S_n-n\mu}{\sqrt{n}\sigma}\xrightarrow{d}N(0,1).
$$

特殊情形包括

- De Moivre-Laplace 定理，二项分布标准化后收敛到标准正态。
- 泊松分布标准化后也收敛到标准正态。

Berry-Esseen 定理给出收敛速度。若 $E(|X_i-\mu|^3) \lt +\infty$ ，则对任意 $x$ 有

$$
\left|
P\left(\frac{S_n-n\mu}{\sqrt{n}\sigma}\leq x\right)-\Phi(x)
\right|
\leq
O(1)\frac{E(|X_i-\mu|^3)}{\sigma^3\sqrt{n}}.
$$

## 应用

集中不等式常先控制单个事件的失败概率，再由 Union Bound 同时处理一族事件。

### 重复运行降低失败概率

若程序单次以 $\frac{2}{3}$ 的概率返回正确结果，独立运行 $t$ 次，只要有一次成功就接受，则失败概率为

$$
\left(\frac{1}{3}\right)^t.
$$

取

$$
t=O\left(\log\frac{1}{\delta}\right)
$$

即可把失败概率降到 $\delta$ 以内。

若单次正确答案概率为 $\frac{2}{3}$ ，但错误答案可能有多种，则重复运行 $T$ 次并取出现频率最高的答案。令 $X$ 为错误次数，则 $X\sim B(T,\frac{1}{3})$ 。错误答案成为多数需要 $X\geq \frac{T}{2}$ ，由 Chernoff bound 可知

$$
P\left(X\geq \frac{T}{2}\right)\leq e^{-\Omega(T)}.
$$

### 随机快速排序

令 $C_{ij}$ 表示排序过程中元素 $i$ 与 $j$ 是否被比较。若 $i \lt j$ ，则它们被比较当且仅当区间 $\lbrace i,i+1,\ldots,j\rbrace$ 中第一个被选为主元的元素是 $i$ 或 $j$ 。因此

$$
P(C_{ij})=\frac{2}{j-i+1}.
$$

于是总比较次数 $T$ 满足

$$
E(T)=O\left(\sum_{i \lt j}\frac{2}{j-i+1}\right)=O(n\log n).
$$

进一步可以用 Chernoff-Hoeffding 控制单个元素的比较次数，再用 union bound 得到高概率的 $O(n\log n)$ 时间界。

### Discrepancy

给定集合族 $S_1,\ldots,S_m\subseteq \lbrace 1,\ldots,n\rbrace$ ，随机把每个元素染成 $+1$ 或 $-1$ 。对固定集合 $S_i$ ，定义

$$
\mathrm{disc}_\chi(S_i)=\left|\sum_{j\in S_i}\chi(j)\right|.
$$

由 Chernoff-Hoeffding 不等式

$$
P(\mathrm{disc}_\chi(S_i)\geq k)\leq 2e^{-k^2/(2n)}.
$$

再对 $m$ 个集合使用 union bound，取

$$
k=\Theta(\sqrt{n\log m})
$$

可得存在一种染色，使所有集合的 discrepancy 都不超过该量级。

### Johnson-Lindenstrauss 引理

Johnson-Lindenstrauss 引理说明，高维点集经过随机线性映射后，可以在较低维空间中近似保持所有点对距离。

给定 $x_1,\ldots,x_n\in \mathbb{R}^d$ ，希望构造低维映射 $F:\mathbb{R}^d\to \mathbb{R}^k$ ，使所有点对距离近似保持

$$
(1-\epsilon)\|x_i-x_j\|_2^2
\leq
\|F(x_i)-F(x_j)\|_2^2
\leq
(1+\epsilon)\|x_i-x_j\|_2^2.
$$

构造随机矩阵 $A\in \mathbb{R}^{k\times d}$ ，其元素独立同分布且服从 $N(0,1)$ ，令

$$
F(x)=\frac{1}{\sqrt{k}}Ax.
$$

对固定向量 $\Delta=x_i-x_j$ ，有 $A\Delta$ 的每个坐标独立服从 $N(0,\|\Delta\|_2^2)$ ，因此

$$
\frac{\|A\Delta\|_2^2}{\|\Delta\|_2^2}\sim \chi_k^2.
$$

利用卡方分布的集中不等式可得

$$
P\left(
\left\|\frac{1}{\sqrt{k}}A\Delta\right\|_2^2
\notin
(1\pm \epsilon)\|\Delta\|_2^2
\right)
\leq
2e^{-k\epsilon^2/8}.
$$

对全部点对使用 union bound，只需

$$
k=O\left(\frac{\log n}{\epsilon^2}\right)
$$

即可使所有点对距离同时得到保持。所需维度只与点数 $n$ 的对数有关，与原维度 $d$ 无关。
