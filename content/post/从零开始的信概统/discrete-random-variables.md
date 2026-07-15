---
title: 离散随机变量
date: 2026-01-02
categories:
    - 数学
slug: 离散随机变量
hidden: true
seriesOrder: 2
---

随机变量把样本点映射为实数，使概率问题可以进一步讨论取值分布、平均位置和波动大小。

## 随机变量的定义

给定样本空间 $S$ ，随机变量是定义在 $S$ 上的实值函数 $X:S\to \mathbb{R}$ 。
通常用大写字母 $X,Y,Z$ 表示随机变量。

对某个取值 $x$ ，事件 $\lbrace X=x\rbrace$ 表示 $\lbrace e\in S:X(e)=x\rbrace$ 。
于是

$$
P(X=x)=P(\lbrace e:X(e)=x\rbrace)
$$

同一取值的原像构成样本空间的一块，因此可以按取值写出分布列。

## 离散随机变量的分布列

离散随机变量只取有限个或可列个值。若 $X$ 的可能取值为 $x_1,x_2,\ldots$ ，记

$$
p_i=P(X=x_i)
$$

则 $\lbrace p_i\rbrace$ 称为 $X$ 的概率分布列，并满足

$$
p_i\geq 0,\qquad \sum_i p_i=1
$$

若进行 $n$ 重 Bernoulli 试验，事件 $A$ 每次发生概率为 $p$ ，令 $X$ 为 $A$ 发生次数，则

$$
P(X=k)=\binom{n}{k}p^k(1-p)^{n-k},\qquad 0\leq k\leq n
$$

这就是二项分布。

以两枚硬币为例。单枚硬币出现正面的概率为 $p$ ，令 $X$ 表示正面数量，则

$$
P(X=0)=(1-p)^2
$$

$$
P(X=1)=2p(1-p)
$$

$$
P(X=2)=p^2
$$

## 随机变量函数的分布

给定离散随机变量 $X$ 和函数 $g$ ，令 $Y=g(X)$ 。
若 $P(X=x_i)=p_i$ ，则

$$
P(Y=g(x_i))=p_i
$$

如果不同的 $x_i$ 映到同一个值，需要把对应概率相加。

设

$$
P(X=1)=0.1,\qquad
P(X=-1)=0.1,\qquad
P(X=0)=0.8
$$

令 $Y=X^2$ ，则

$$
P(Y=1)=0.2,\qquad P(Y=0)=0.8
$$

因为 $X=1$ 和 $X=-1$ 都会映到 $Y=1$ 。

## 数学期望

数学期望描述随机变量的平均取值。离散随机变量 $X$ 满足绝对收敛条件

$$
\sum_i |x_i|p_i \lt +\infty
$$

时，定义

$$
E(X)=\sum_i x_ip_i
$$

分布列的概率和为 $1$ 并不能保证期望有限，因此定义中需要绝对收敛条件。

设有两个奖金增长方式不同的闯关游戏。

第一个游戏初始奖金为 $1$ 元，每多闯一关多得 $1$ 元，通过每关概率为 $1/2$ 。若 $X$ 为最终奖金，则

$$
P(X=k)=\frac{1}{2^k},\qquad k\geq 1
$$

所以

$$
E(X)=\sum_{k\geq 1}\frac{k}{2^k}=2
$$

第二个游戏初始奖金为 $0.5$ 元，每多闯一关奖金翻倍。此时奖金为 $2^{k-2}$ 的概率为 $2^{-k}$ ，期望为

$$
\sum_{k\geq 1}2^{k-2}\cdot 2^{-k}=+\infty
$$

第二个游戏虽然以较大概率得到较少奖金，但奖金增长足以使期望发散。

二项分布的期望和二阶矩可以直接由分布列求得。若 $X\sim B(n,p)$ ，则

$$
E(X)=\sum_{k=0}^{n}k\binom{n}{k}p^k(1-p)^{n-k}=np
$$

二阶矩常用 $k^2=k(k-1)+k$ 拆开

$$
E(X^2)-E(X)
=\sum_{k=0}^{n}k(k-1)\binom{n}{k}p^k(1-p)^{n-k}
$$

因此

$$
E(X^2)=n(n-1)p^2+np
$$

于是

$$
\mathrm{Var}(X)=np(1-p)
$$

对随机变量函数也可以直接算期望

$$
E(g(X))=\sum_i p_i g(x_i)
$$

常用性质

- 若 $P(X=c)=1$ ，则 $E(X)=c$
- $E(aX+b)=aE(X)+b$
- $E(g_1(X)\pm g_2(X))=E(g_1(X))\pm E(g_2(X))$

对事件 $A$ ，示性函数 $\mathbf{1}_A$ 定义为事件发生时取 $1$ ，否则取 $0$ 。于是 $P(A)=E(\mathbf{1}_A)$
遇到计数问题时，把总数拆成若干个示性函数，通常比直接数简单。

期望还有两个小结论

$$
P(X\geq E(X)) \gt 0,\qquad P(X\leq E(X)) \gt 0
$$

它们常用于概率证法。

随机分组问题可以直接使用示性函数。

有 $n$ 个人，其中有 $m$ 对人认识。把每个人等概率分到两组，令 $X$ 表示分在不同组且认识的对数。

对每一对认识的人，被分开的概率都是 $1/2$ ，所以

$$
E(X)=\frac{m}{2}
$$

由 $P(X\geq E(X)) \gt 0$ 可知，存在一种分组使得至少 $m/2$ 对认识的人被分开。

## Markov 不等式

若 $X$ 为非负随机变量，且 $E(X) \gt 0$ ，则对 $a \gt 0$ 有

$$
P(X\geq aE(X))\leq \frac{1}{a}
$$

在期望中只保留满足 $X\geq aE(X)$ 的部分，可得

$$
E(X)\geq aE(X)P(X\geq aE(X))
$$

Markov 不等式的条件很弱，所以界通常比较松；但它是很多尾界的起点。

例如，只用期望估计硬币正面数的上尾概率。

投 $n$ 枚公平硬币，令 $X$ 为正面数。则 $E(X)=n/2$ 。想估计正面超过 $3n/4$ 的概率，Markov 给出

$$
P\left(X\geq \frac{3n}{4}\right)
=P\left(X\geq \frac{3}{2}E(X)\right)
\leq \frac{2}{3}
$$

这个界很松，但只用了 $X\geq 0$ 和期望。

## 方差

期望看平均位置，方差看波动大小。若 $E((X-E(X))^2)$ 存在，定义 $\mathrm{Var}(X)=E((X-E(X))^2)$
标准差定义为

$$
\sigma(X)=\sqrt{\mathrm{Var}(X)}
$$

标准差和随机变量本身同量纲，比方差更方便直接解释。

常用性质

$$
\mathrm{Var}(aX+b)=a^2\mathrm{Var}(X)
$$

$$
\sigma(aX+b)=|a|\sigma(X)
$$

$$
\mathrm{Var}(X)=E(X^2)-(E(X))^2
$$

因此

$$
E(X^2)\geq (E(X))^2
$$

若 $X\sim B(n,p)$ ，则

$$
\mathrm{Var}(X)=np(1-p),\qquad
\sigma(X)=\sqrt{np(1-p)}
$$

## Chebyshev 不等式

若 $\sigma(X) \gt 0$ ，则对任意 $c \gt 0$ 有

$$
P(|X-E(X)|\geq c\sigma(X))\leq \frac{1}{c^2}
$$

对非负随机变量 $(X-E(X))^2$ 使用 Markov 不等式即可得到证明。Chebyshev 使用了二阶矩，估计偏离期望的概率时通常比只使用一阶矩的 Markov 更紧。若目标事件是单侧偏离，还需要结合分布的对称性或直接比较事件包含关系。

对同一个硬币问题，Chebyshev 可以给出随 $n$ 衰减的上界。

同样投 $n$ 枚公平硬币， $X\sim B(n,1/2)$ ，所以

$$
E(X)=\frac{n}{2},\qquad
\mathrm{Var}(X)=\frac{n}{4}
$$

若正面超过 $3n/4$ ，则至少偏离期望 $n/4$ 。Chebyshev 给出

$$
P\left(\left|X-E(X)\right|\geq \frac{n}{4}\right)
\leq \frac{\mathrm{Var}(X)}{(n/4)^2}
=\frac{4}{n}
$$

如果只要单侧事件，还可以再观察对称性得到更紧的估计。

同样的方法可以估计成绩达到优秀线的比例。

某课程平均分为 $70$ ，优秀线为 $90$ 。若只知道平均分，用 Markov 不等式

$$
P(X\geq 90)
=P\left(X\geq \frac{9}{7}E(X)\right)
\leq \frac{7}{9}
$$

若还知道标准差为 $5$ ，用 Chebyshev

$$
P(X\geq 90)
\leq P(|X-70|\geq 20)
\leq \frac{1}{16}
$$

方差信息将上界从 $7/9$ 收紧到了 $1/16$ 。

## 常用离散分布

### Bernoulli 分布

单次 Bernoulli 试验的结果服从 Bernoulli 分布。随机变量 $X$ 只取 $0$ 和 $1$ ，且

$$
P(X=1)=p,\qquad P(X=0)=1-p
$$

记作 $X\sim B(1,p)$ ，也叫 $0$ - $1$ 分布或两点分布。

### 二项分布

$n$ 重 Bernoulli 试验中成功次数服从二项分布，记作 $X\sim B(n,p)$ 。分布列为

$$
P(X=k)=\binom{n}{k}p^k(1-p)^{n-k}
$$

并且

$$
E(X)=np,\qquad \mathrm{Var}(X)=np(1-p)
$$

### Poisson 分布

若随机变量 $X$ 取非负整数，且

$$
P(X=k)=\frac{\lambda^k}{k!}e^{-\lambda},\qquad \lambda \gt 0
$$

则称 $X$ 服从参数为 $\lambda$ 的 Poisson 分布，记作

$$
X\sim \pi(\lambda)
$$

它满足

$$
E(X)=\lambda,\qquad E(X^2)=\lambda^2+\lambda,\qquad
\mathrm{Var}(X)=\lambda
$$

Poisson 定理说，若 $np_n\to \lambda$ ，则对固定的 $k$ 有

$$
\binom{n}{k}p_n^k(1-p_n)^{n-k}
\to \frac{\lambda^k}{k!}e^{-\lambda}
$$

因此 Poisson 分布可以看作成功概率很小、试验次数很大时二项分布的极限。令 $\lambda_n=np_n$ 后，可以把二项分布的概率质量函数拆成若干个分别收敛的因子。

球桶模型给出了一个典型的 Poisson 近似。

第 $i$ 个桶中球数满足

$$
X_i\sim B\left(n,\frac{1}{m}\right)
$$

若 $n=\lambda m$ 且 $m\to+\infty$ ，则

$$
P(X_i=k)
=\binom{n}{k}\left(\frac{1}{m}\right)^k
\left(1-\frac{1}{m}\right)^{n-k}
\approx \frac{\lambda^k}{k!}e^{-\lambda}
$$

### 几何分布

几何分布描述第一次成功所需的试验次数。若每次成功概率为 $p$ ，则

$$
P(X=k)=p(1-p)^{k-1},\qquad k\geq 1
$$

记作 $X\sim G(p)$ 。它满足

$$
E(X)=\frac{1}{p}
$$

$$
E(X^2)=\frac{2(1-p)}{p^2}+\frac{1}{p}
$$

$$
\mathrm{Var}(X)=\frac{1-p}{p^2}
$$

几何分布的重要性质是无记忆性

$$
P(X \gt m+n\mid X \gt m)=P(X \gt n)
$$

因为

$$
P(X \gt n)=(1-p)^n
$$

### 负二项分布

负二项分布描述第 $r$ 次成功出现时的试验次数。若 $k\geq r$ ，则

$$
P(X=k)=\binom{k-1}{r-1}p^r(1-p)^{k-r}
$$

记作 $X\sim NB(r,p)$ 。当 $r=1$ 时，它就是几何分布。

若 $X_1,\ldots,X_r$ 独立同分布，且 $X_i\sim G(p)$
则

$$
X_1+\cdots+X_r\sim NB(r,p)
$$

等待第 $r$ 次成功的总时间，可以拆成 $r$ 段相互独立的几何等待时间。

负二项分布的归一化可以由级数恒等式验证。

若 $X\sim NB(r,p)$ ，需要验证分布列求和为 $1$ 。令 $l=k-r$ ，则

$$
\sum_{k\geq r}\binom{k-1}{r-1}p^r(1-p)^{k-r}
=p^r\sum_{l\geq 0}\binom{l+r-1}{r-1}(1-p)^l
$$

由负二项展开

$$
\sum_{l\geq 0}\binom{l+r-1}{r-1}(1-p)^l=p^{-r}
$$

因此总和为 $1$ 。
