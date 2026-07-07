---
title: 尾不等式、大数定律和中心极限定理
date: 2026-01-02
categories:
    - 数学
slug: 尾不等式、大数定律和中心极限定理
hidden: true
seriesOrder: 6
---

这节主要是在攒尾界工具。Markov 和 Chebyshev 够通用，但经常偏松；Chernoff 和 Hoeffding 多用了独立性，所以在随机算法里更常见。大数定律回答“样本平均会不会稳”，中心极限定理回答“标准化以后大概长什么样”。

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

这两个不等式要求很低，因此也不要指望界特别紧。它们更像是最基础的保底工具。

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

这已经能推出

$$
\lim_{n\to+\infty}P(|f_n(A)-p| \lt \epsilon)=1.
$$

但 Chebyshev 只使用到二阶矩，实际上只需要两两独立，不能充分利用全部独立性。

## 高阶矩方法

如果二阶矩给得太松，自然会想到四阶矩。偶数阶中心矩是非负的，所以仍然能套 Markov。

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

这比 Chebyshev 更强，但仍然没有完全发挥独立性。

## Chernoff Bound

Chernoff 的思路是把 $X$ 放进指数里。指数函数会放大尾部，因此只要矩生成函数可控，得到的界通常会比多项式矩强很多。

Chernoff bound 的做法是对 $e^{tX}$ 使用 Markov 不等式。若 $t \gt 0$ ，则

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

Hoeffding 引理负责处理“有界”这个条件。和 Chernoff 合起来之后，就能得到最常用的独立有界随机变量集中不等式。

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

证明套路是

1. 对 $X-E(X)$ 使用 Chernoff bound。
2. 利用独立性把矩生成函数拆成乘积。
3. 对每一项使用 Hoeffding 引理。
4. 对 $t$ 求最优值。

## 大数定律

大数定律说的是样本平均的稳定性。这里的稳定是依概率意义下的，不是说每一条样本路径都一定收敛。

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

证明直接使用 Chebyshev 不等式。

一个常见例子，若 $X_i$ 同分布，且每个 $X_i$ 只与 $X_{i-1}$ 和 $X_{i+1}$ 可能相关，其余不相关，则

$$
\mathrm{Var}\left(\sum_{i=1}^{n}X_i\right)=O(n),
$$

因此满足 Markov 大数定律。

### Khinchin 大数定律

若 $X_1,X_2,\ldots$ 独立同分布，且 $E(X_i)=\mu$ 存在，则

$$
\frac{1}{n}\sum_{i=1}^{n}X_i\xrightarrow{P}\mu.
$$

这里不要求方差存在。

## 随机变量序列的收敛

这里主要区分依概率收敛和依分布收敛。前者更强，后者只要求分布函数意义下靠近。

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

特征函数这块比较抽象，但它的优点很明显，总是存在，而且独立随机变量求和会变成乘积。

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

因此独立同分布柯西随机变量的平均值仍服从同一个柯西分布，这也是 Khinchin 大数定律中“期望存在”假设不可少的典型例子。

## 中心极限定理

大数定律只说平均值会靠近均值，中心极限定理进一步告诉我们“靠近时的波动形状”。

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

## 应用举例

后面的例子基本都在做同一件事，先证明单个事件失败概率很小，再用 union bound 处理所有事件。

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

随机投影这部分很漂亮，一个高维点集被随机矩阵打到低维之后，所有点对距离仍然能同时保持。

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

即可使所有点对距离同时被保持。最终维度只与点数 $n$ 的对数有关，与原维度 $d$ 无关。
