---
title: 连续随机变量
date: 2026-01-02
categories:
    - 数学
slug: 连续随机变量
hidden: true
seriesOrder: 3
---

连续随机变量的概率由区间上的积分给出，密度值本身不是概率。单点概率为 $0$ 只表示概率质量不会集中在一个点上。

## 分布函数

对任意随机变量 $X$ ，分布函数定义为

$$
F(x)=P(X\leq x)
$$

它有三条基本性质。

- 有界性

$$
0\leq F(x)\leq 1,\qquad
\lim_{x\to-\infty}F(x)=0,\qquad
\lim_{x\to+\infty}F(x)=1
$$

- 单调性， $F(x)$ 关于 $x$ 单调不减
- 右连续，对任意 $x_0$ ，有

$$
F(x_0+0)=F(x_0)
$$

分布函数不一定左连续。离散随机变量的分布函数在有质量的点处会跳跃。

若把定义中的“小于等于”改为“小于”，得到的函数将左连续。这里的左右连续性与高数中的间断点分类一致。

利用分布函数求概率时，左右端点要看清楚

$$
P(a \lt X\leq b)=F(b)-F(a)
$$

$$
P(a\leq X\leq b)=F(b)-F(a-0)
$$

$$
P(X=a)=F(a)-F(a-0)
$$

$$
P(X\geq a)=1-F(a-0)
$$

如果 $X$ 是连续随机变量，则 $F$ 连续，这些公式里的左右开闭就不再影响概率。

圆内随机点到圆心的距离可以先求分布函数。

在半径为 $r$ 的圆内均匀取一点，令 $X$ 表示它到圆心的距离。对 $0\leq x\leq r$ ，有

$$
F(x)=P(X\leq x)=\frac{\pi x^2}{\pi r^2}=\frac{x^2}{r^2}
$$

因此密度为

$$
f(x)=\frac{2x}{r^2},\qquad 0 \lt x \lt r
$$

若 $X\sim U(0,1)$ ，则其分布函数为

$$
F(x)=
\begin{cases}
0, & x\leq 0, \\
x, & 0 \lt x \lt 1, \\
1, & x\geq 1.
\end{cases}
$$

函数在 $0$ 和 $1$ 处连续。

Bernoulli 分布则表现为阶梯状的分布函数。

若 $X\sim B(1,p)$ ，则

$$
F(x)=
\begin{cases}
0, & x \lt 0, \\
1-p, & 0\leq x \lt 1, \\
1, & x\geq 1.
\end{cases}
$$

它在 $0$ 和 $1$ 处跳跃，所以不是连续随机变量。

## 概率密度函数

若存在非负函数 $f$ ，使得

$$
F(x)=\int_{-\infty}^{x}f(t)\,dt
$$

则称 $X$ 为连续随机变量， $f$ 为它的概率密度函数。

密度函数满足

$$
f(x)\geq 0
$$

$$
\int_{-\infty}^{+\infty}f(t)\,dt=1
$$

在 $F$ 可导的点，有

$$
F'(x)=f(x)
$$

连续随机变量的分布函数一定连续，所以

$$
P(X=a)=0
$$

也因此，对连续随机变量有

$$
P(a \lt X\leq b)=P(a\leq X\leq b)=P(a \lt X \lt b)=P(a\leq X \lt b)
$$

概率密度函数和分布函数不完全一一对应。把密度函数在有限个点上的值随便改掉，积分不变，分布函数也不变。

以 Cauchy 密度为例，同时检查期望的存在性。

设

$$
f(x)=\frac{c}{1+x^2}
$$

要求它是密度函数，需要

$$
\int_{-\infty}^{+\infty}\frac{c}{1+x^2}\,dx=1
$$

所以

$$
c=\frac{1}{\pi}
$$

分布函数为

$$
F(x)=\frac{\arctan x}{\pi}+\frac{1}{2}
$$

但它的数学期望不存在，因为

$$
\int_{-\infty}^{+\infty}|x|f(x)\,dx=+\infty
$$

所以合法密度不保证期望存在。

## 数学期望和方差

若

$$
\int_{-\infty}^{+\infty}|x|f(x)\,dx \lt +\infty
$$

则连续随机变量 $X$ 的数学期望为

$$
E(X)=\int_{-\infty}^{+\infty}x f(x)\,dx
$$

计算期望前需要先检查绝对可积性。对函数 $g(X)$ ，可以直接使用

$$
E(g(X))=\int_{-\infty}^{+\infty}g(x)f(x)\,dx
$$

直接算 $E(X^2)$ 时，不必先求 $X^2$ 的密度。

若 $X\sim U(0,1)$ ，求 $E(X^2)$ 时无须先求 $Y=X^2$ 的密度

$$
E(X^2)=\int_0^1 x^2\,dx=\frac{1}{3}
$$

期望的线性性仍然成立 $E(aX+b)=aE(X)+b$

$$
E(g_1(X)\pm g_2(X))
=E(g_1(X))\pm E(g_2(X))
$$

Markov 不等式也仍然成立，若 $X\geq 0$ 且 $E(X) \gt 0$ ，则

$$
P(X\geq aE(X))\leq \frac{1}{a}
$$

方差定义为

$$
\mathrm{Var}(X)=E((X-E(X))^2)
$$

标准差为

$$
\sigma(X)=\sqrt{\mathrm{Var}(X)}
$$

常用公式和离散情形一致

$$
\mathrm{Var}(aX+b)=a^2\mathrm{Var}(X)
$$

$$
\mathrm{Var}(X)=E(X^2)-(E(X))^2
$$

Chebyshev 不等式也同样成立

$$
P(|X-E(X)|\geq c\sigma(X))\leq \frac{1}{c^2}
$$

## 常用连续分布

### 均匀分布

若 $X$ 在区间 $(a,b)$ 上均匀分布，记作 $X\sim U(a,b)$
密度函数为

$$
f(x)=
\begin{cases}
\dfrac{1}{b-a}, & a \lt x \lt b, \\
0, & \text{其他}.
\end{cases}
$$

期望和方差为

$$
E(X)=\frac{a+b}{2}
$$

$$
\mathrm{Var}(X)=\frac{(b-a)^2}{12}
$$

### 正态分布

标准正态分布的密度为

$$
f(x)=\frac{1}{\sqrt{2\pi}}e^{-x^2/2}
$$

记作 $X\sim N(0,1)$ 。它关于 $0$ 对称，最大值在 $0$ 处取得，并满足

$$
E(X)=0,\qquad \mathrm{Var}(X)=1
$$

标准正态分布没有初等形式的分布函数，但有常用数值

$$
P(|X|\leq 2)=0.9545
$$

$$
P(|X|\leq 3)=0.9973
$$

一般正态分布的密度为

$$
f(x)=\frac{1}{\sqrt{2\pi}\sigma}
e^{-\frac{(x-\mu)^2}{2\sigma^2}}
$$

记作

$$
X\sim N(\mu,\sigma^2)
$$

若 $X\sim N(\mu,\sigma^2)$ ，则标准化随机变量

$$
U=\frac{X-\mu}{\sigma}
$$

满足

$$
U\sim N(0,1)
$$

因此

$$
E(X)=\mu,\qquad
\mathrm{Var}(X)=\sigma^2
$$

一般随机变量也可以标准化。若 $E(X)=\mu$ 且 $\sigma(X)=\sigma \gt 0$ ，令

$$
Y=\frac{X-\mu}{\sigma}
$$

则

$$
E(Y)=0,\qquad \mathrm{Var}(Y)=1
$$

当 $X\sim B(1,1/2)$ 时，标准化后得到 Rademacher 分布

$$
P(Y=1)=P(Y=-1)=\frac{1}{2}
$$

### 指数分布

若 $\lambda \gt 0$ ，指数分布的密度为

$$
f(x)=
\begin{cases}
\lambda e^{-\lambda x}, & x\geq 0, \\
0, & x \lt 0.
\end{cases}
$$

记作

$$
X\sim \mathrm{Exp}(\lambda)
$$

分布函数为

$$
F(x)=
\begin{cases}
1-e^{-\lambda x}, & x\geq 0, \\
0, & x \lt 0.
\end{cases}
$$

它满足

$$
E(X)=\frac{1}{\lambda},\qquad
\mathrm{Var}(X)=\frac{1}{\lambda^2}
$$

指数分布是几何分布在连续时间里的对应物，也有无记忆性

$$
P(X \gt s+t\mid X \gt s)=P(X \gt t)
$$

指数分布可以由 Poisson 过程中的等待时间导出。

用 $N(t)$ 表示时间 $t$ 内设备故障次数，假设 $N(t)\sim \pi(\lambda t)$
第一次发生故障的时间记作 $X$ 。则

$$
P(X\leq t)=P(N(t)\geq 1)=1-e^{-\lambda t}
$$

因此

$$
X\sim \mathrm{Exp}(\lambda)
$$

分布函数中的补事件给出 $1-e^{-\lambda t}$ 。

### Gamma 分布

Gamma 函数定义为

$$
\Gamma(\alpha)=\int_{0}^{+\infty}x^{\alpha-1}e^{-x}\,dx,\qquad \alpha \gt 0
$$

常用性质

$$
\Gamma(\alpha+1)=\alpha\Gamma(\alpha)
$$

$$
\Gamma(n+1)=n!
$$

$$
\Gamma\left(n+\frac{1}{2}\right)
=\frac{(2n)!}{4^n n!}\sqrt{\pi}
$$

若 $\alpha,\lambda \gt 0$ ，定义密度

$$
f(x)=
\begin{cases}
\dfrac{\lambda^\alpha}{\Gamma(\alpha)}
x^{\alpha-1}e^{-\lambda x}, & x\geq 0, \\
0, & x \lt 0.
\end{cases}
$$

则称

$$
X\sim \Gamma(\alpha,\lambda)
$$

$\lambda$ 采用 rate 参数化，因此

$$
E(X)=\frac{\alpha}{\lambda}
$$

$$
E(X^2)=\frac{\alpha(\alpha+1)}{\lambda^2}
$$

$$
\mathrm{Var}(X)=\frac{\alpha}{\lambda^2}
$$

当 $\alpha=1$ 时，Gamma 分布退化为指数分布。当

$$
\alpha=\frac{n}{2},\qquad \lambda=\frac{1}{2}
$$

时，得到自由度为 $n$ 的 $\chi^2$ 分布，记作 $\chi^2(n)$ ，并且

$$
E(X)=n,\qquad \mathrm{Var}(X)=2n
$$

若 $N(t)\sim \pi(\lambda t)$ ，记第 $n$ 次故障时间为 $X$ ，则

$$
P(X\leq t)=P(N(t)\geq n)
=1-\sum_{k=0}^{n-1}\frac{e^{-\lambda t}(\lambda t)^k}{k!}
$$

对分布函数求导可得密度

$$
f(x)=\frac{x^{n-1}\lambda^n e^{-\lambda x}}{(n-1)!},\qquad x\geq 0
$$

因此 $X\sim \Gamma(n,\lambda)$ 。

## 连续随机变量函数的分布

给定连续随机变量 $X$ 和函数 $g$ ，可以先写出 $Y=g(X)$ 的分布函数，再由求导得到密度。

若 $g$ 严格单调，反函数为 $h$ ，且 $h$ 有连续导数，则 $f_Y(y)=f_X(h(y))|h'(y)|$ 。其中 $|h'(y)|$ 是 Jacobian 因子。若 $g$ 不单调，则需要分别计算各个反函数分支的贡献。

考虑变换 $Y=|X|$ 。

若 $X\sim U(-4,4)$ ，令 $Y=|X|$ 。对 $0 \lt y \lt 4$ ， $y$ 和 $-y$ 两个点都会贡献概率。由分布函数可得

$$
P(Y\leq y)=P(-y\leq X\leq y)=\frac{2y}{8}=\frac{y}{4}
$$

因此

$$
f_Y(y)=\frac{1}{4},\qquad 0 \lt y \lt 4
$$

再考虑线性变换 $Y=2X$ 。

若 $X\sim U(-4,4)$ ，令 $Y=2X$ 。变换后的区间长度翻倍，密度相应减半。由变量变换

$$
h(y)=\frac{y}{2},\qquad |h'(y)|=\frac{1}{2}
$$

于是

$$
f_Y(y)=f_X\left(\frac{y}{2}\right)\frac{1}{2}
=\frac{1}{16},\qquad -8 \lt y \lt 8
$$

正态分布的仿射变换也很常用。

若 $X\sim N(\mu,\sigma^2)$ 且 $a\neq 0$ ，令 $Y=aX+b$ ，则 $Y\sim N(a\mu+b,a^2\sigma^2)$ 。反函数为

$$
h(y)=\frac{y-b}{a}
$$

变量变换里的绝对值会把 $a$ 变成 $|a|$ ，最后方差里出现 $a^2$ 。

Gamma 分布伸缩时，rate 参数也随之变化。

若 $X\sim \Gamma(\alpha,\lambda)$ 且 $k \gt 0$ ，令 $Y=kX$ ，则

$$
Y\sim \Gamma\left(\alpha,\frac{\lambda}{k}\right)
$$

将随机变量放大 $k$ 倍时，rate 缩小为原来的 $1/k$ 。

若 $X$ 的密度满足

$$
f_X(x)=\frac{2x}{\pi^2},\qquad 0 \lt x \lt \pi
$$

令 $Y=\sin X$ 。由于 $\sin x$ 在 $(0,\pi)$ 上有两个反函数分支，对 $0 \lt y \lt 1$ 有

$$
\sin x\leq y
\quad\Longleftrightarrow\quad
x\in (0,\arcsin y)\cup(\pi-\arcsin y,\pi)
$$

两条分支的密度贡献相加，得到

$$
f_Y(y)=\frac{2}{\pi\sqrt{1-y^2}},\qquad 0 \lt y \lt 1
$$
