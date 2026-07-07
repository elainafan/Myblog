---
title: 多维连续随机变量
date: 2026-01-02
categories:
    - 数学
slug: 多维连续随机变量
hidden: true
seriesOrder: 5
---

记号变多以后，很容易把联合、边际、条件这三件事混在一起。这里按“联合分布 $\rightarrow$ 边际分布 $\rightarrow$ 条件分布 $\rightarrow$ 函数变换 $\rightarrow$ 多维高斯”的顺序整理。做题时大多也是这个顺序，先看区域，再选积分顺序；如果是变量变换，再去算 Jacobian。

## 线性代数速记

这部分线代不是重点，但后面多维高斯会一直用到。先把会出现的词放在这里，免得读到协方差矩阵的时候再回头翻。

- 特征值与特征向量，若 $x\neq 0$ 且 $Ax=\lambda x$ ，则 $\lambda$ 是 $A$ 的特征值， $x$ 是对应特征向量。
- 若 $A$ 可对角化，则 $A=P\Lambda P^{-1}$ ，其中 $P$ 的列向量为特征向量， $\Lambda$ 为特征值组成的对角矩阵。
- $\det(A)=\prod_i\lambda_i$ ， $\mathrm{tr}(A)=\sum_i\lambda_i$ 。
- 对称矩阵满足 $A^\top=A$ ，其特征值均为实数，并且不同特征值对应的特征向量正交。
- 正交矩阵满足 $U^\top U=UU^\top=I$ ，并保持欧氏长度不变，即 $\|Ux\|_2=\|x\|_2$ 。
- 对称矩阵的谱分解为 $A=U\Lambda U^\top$ 。
- 半正定矩阵满足 $x^\top Ax\geq 0$ ，等价于所有特征值非负。
- 正定矩阵满足 $x^\top Ax \gt 0$ ，等价于所有特征值为正。
- 若 $A$ 半正定，则存在 $A^{1/2}$ 使得 $A^{1/2}A^{1/2}=A$ 。

## 联合分布函数与联合密度

给定二维随机变量 $X,Y$ ，定义联合分布函数

$$
F(x,y)=P(X\leq x,Y\leq y).
$$

它满足以下性质

- 有界性， $0\leq F(x,y)\leq 1$ ，且 $F(-\infty,y)=F(x,-\infty)=0$ ， $F(+\infty,+\infty)=1$ 。
- 单调性，关于每个变量分别单调不减。
- 右连续性， $F(x+0,y)=F(x,y)$ ， $F(x,y+0)=F(x,y)$ 。
- 矩形非负性

$$
P(a \lt X\leq b,c \lt Y\leq d)=F(b,d)-F(a,d)-F(b,c)+F(a,c)\geq 0.
$$

若存在非负函数 $f(x,y)$ 使得

$$
F(x,y)=\int_{-\infty}^{x}\int_{-\infty}^{y}f(u,v)\,dv\,du,
$$

则称 $(X,Y)$ 为二维连续随机变量， $f(x,y)$ 为联合密度函数。联合密度满足

$$
\int_{-\infty}^{+\infty}\int_{-\infty}^{+\infty}f(x,y)\,dx\,dy=1.
$$

对区域 $G$ ，有

$$
P((X,Y)\in G)=\iint_G f(x,y)\,dx\,dy.
$$

二维指数型联合密度主要练积分区域。

密度题通常不要急着化简。先用正则性把常数定出来，再把事件翻译成积分区域。

若

$$
f(x,y)=
\begin{cases}
ce^{-2x-3y}, & x \gt 0,\ y \gt 0, \\
0, & \text{其他},
\end{cases}
$$

由正则性得到

$$
c=6
$$

因此

$$
P(X \lt 1,Y \gt 1)=\int_0^1\int_1^{+\infty}6e^{-2x-3y}\,dy\,dx=(1-e^{-2})e^{-3}
$$

又

$$
P(X \gt Y)=\int_0^{+\infty}\int_0^x6e^{-2x-3y}\,dy\,dx=\frac{3}{5}
$$

重点还是积分区域，先画区域再选积分顺序。

有界区域上的均匀分布，本质上就是面积比。

若 $(X,Y)$ 在有界区域 $D$ 上均匀分布，则

$$
f(x,y)=
\begin{cases}
\frac{1}{S_D}, & (x,y)\in D, \\
0, & (x,y)\notin D,
\end{cases}
$$

其中 $S_D$ 是区域 $D$ 的面积。概率就是对应子区域面积除以 $S_D$ 。

## 边际分布与条件分布

边际分布就是“只看一个坐标”。连续情形下，另一个坐标不是求和，而是积分掉。

由联合分布函数得到边际分布函数

$$
F_X(x)=F(x,+\infty),\qquad F_Y(y)=F(+\infty,y).
$$

若联合密度存在，则边际密度为

$$
f_X(x)=\int_{-\infty}^{+\infty}f(x,y)\,dy,\qquad
f_Y(y)=\int_{-\infty}^{+\infty}f(x,y)\,dx.
$$

在 $f_Y(y) \gt 0$ 时，给定 $Y=y$ 条件下 $X$ 的条件密度为

$$
f_{X|Y}(x|y)=\frac{f(x,y)}{f_Y(y)}.
$$

对应的条件分布函数为

$$
F_{X|Y}(x|y)=\int_{-\infty}^{x}\frac{f(u,y)}{f_Y(y)}\,du.
$$

同理，在 $f_X(x) \gt 0$ 时

$$
f_{Y|X}(y|x)=\frac{f(x,y)}{f_X(x)}.
$$

## 独立性

独立性还是老规矩，联合等于边际乘积。只不过连续变量可以用密度函数来判断。

二维随机变量 $X,Y$ 相互独立等价于对任意 $x,y$ 都有

$$
F(x,y)=F_X(x)F_Y(y).
$$

若它们为连续随机变量，也等价于几乎处处有

$$
f(x,y)=f_X(x)f_Y(y).
$$

独立性可以由联合密度是否能拆成两个边际密度的乘积来判断。若联合密度的支撑区域不是两个边际支撑的笛卡尔积，通常就不独立。

## 二维高斯分布

二维高斯的公式看起来很长，但真正要记的东西不多，边际仍是高斯，条件分布仍是高斯， $\rho=0$ 时两个变量独立。

若联合密度为

$$
f(x,y)=\frac{1}{2\pi\sigma_1\sigma_2\sqrt{1-\rho^2}}
\exp\left[
-\frac{1}{2(1-\rho^2)}
\left(
\frac{(x-\mu_1)^2}{\sigma_1^2}
+\frac{(y-\mu_2)^2}{\sigma_2^2}
-\frac{2\rho(x-\mu_1)(y-\mu_2)}{\sigma_1\sigma_2}
\right)
\right],
$$

其中 $\sigma_1,\sigma_2 \gt 0$ 且 $|\rho| \lt 1$ ，则称 $(X,Y)$ 服从二维高斯分布。

边际分布为

$$
X\sim N(\mu_1,\sigma_1^2),\qquad Y\sim N(\mu_2,\sigma_2^2).
$$

条件分布仍为高斯分布

$$
X|Y=y\sim N\left(\mu_1+\rho\frac{\sigma_1}{\sigma_2}(y-\mu_2),\ \sigma_1^2(1-\rho^2)\right),
$$

以及

$$
Y|X=x\sim N\left(\mu_2+\rho\frac{\sigma_2}{\sigma_1}(x-\mu_1),\ \sigma_2^2(1-\rho^2)\right).
$$

二维高斯中， $X$ 与 $Y$ 相互独立当且仅当 $\rho=0$ 。

## 数学期望、协方差与相关系数

这里开始真正关心两个随机变量的关系。协方差只看线性关系，所以独立一定推出不相关，但不相关不一定独立。

对二维连续随机变量，有

$$
E(g(X,Y))=\int_{-\infty}^{+\infty}\int_{-\infty}^{+\infty}g(x,y)f(x,y)\,dx\,dy.
$$

线性性仍成立

$$
E(X+Y)=E(X)+E(Y).
$$

若 $X,Y$ 相互独立，则

$$
E(XY)=E(X)E(Y).
$$

协方差定义为

$$
\mathrm{Cov}(X,Y)=E((X-E(X))(Y-E(Y)))=E(XY)-E(X)E(Y).
$$

常用性质

- $\mathrm{Cov}(X,X)=\mathrm{Var}(X)$ 。
- $\mathrm{Cov}(X,Y)=\mathrm{Cov}(Y,X)$ 。
- $\mathrm{Cov}(aX,bY)=ab\mathrm{Cov}(X,Y)$ 。
- $\mathrm{Cov}(X_1+X_2,Y)=\mathrm{Cov}(X_1,Y)+\mathrm{Cov}(X_2,Y)$ 。
- 独立推出协方差为 $0$ ，但反之不一定成立。

方差展开为

$$
\mathrm{Var}\left(\sum_i X_i\right)=\sum_i\sum_j\mathrm{Cov}(X_i,X_j).
$$

相关系数定义为

$$
\mathrm{Corr}(X,Y)=\frac{\mathrm{Cov}(X,Y)}{\sigma(X)\sigma(Y)}.
$$

它满足

$$
|\mathrm{Corr}(X,Y)|\leq 1.
$$

并且 $\mathrm{Corr}(X,Y)=\pm 1$ 当且仅当 $Y=aX+b$ 几乎必然成立，其中 $a\neq 0$ 。

对二维高斯分布，有

$$
\mathrm{Cov}(X,Y)=\rho\sigma_1\sigma_2,
$$

因此 $\rho$ 就是相关系数。

## 随机变量函数的分布

这类题别只背公式。先问一句，能不能从分布函数直接做？如果不行，再考虑卷积或密度变换。

### 从分布函数出发

求 $Z=g(X,Y)$ 的分布时，常先写

$$
F_Z(z)=P(g(X,Y)\leq z),
$$

再对区域积分或求导得到密度。

最大值与最小值可以直接从分布函数出发。

若 $X,Y$ 独立同分布且均为 $U(0,1)$ ，则对 $0 \lt z \lt 1$ 有

$$
P(\max(X,Y)\leq z)=P(X\leq z,Y\leq z)=z^2
$$

因此 $\max(X,Y)$ 的密度为

$$
2z
$$

类似地

$$
P(\min(X,Y)\leq z)=1-P(X \gt z,Y \gt z)=1-(1-z)^2
$$

### 卷积公式

若 $X,Y$ 相互独立，且 $Z=X+Y$ ，则

$$
f_Z(z)=\int_{-\infty}^{+\infty}f_X(z-y)f_Y(y)\,dy.
$$

指数分布卷积是卷积公式的标准用法。

若 $X,Y$ 独立且均服从 $\mathrm{Exp}(1)$ ，则

$$
f_{X+Y}(z)=\int_0^z e^{-(z-y)}e^{-y}\,dy=ze^{-z},\qquad z \gt 0
$$

所以

$$
X+Y\sim \Gamma(2,1)
$$

算出来正好是 $\Gamma(2,1)$ 。

更一般地，若 $X\sim \Gamma(\alpha_1,\lambda)$ ， $Y\sim \Gamma(\alpha_2,\lambda)$ 且二者独立，则

$$
X+Y\sim \Gamma(\alpha_1+\alpha_2,\lambda).
$$

### 密度变换公式

设

$$
U=u(X,Y),\qquad V=v(X,Y).
$$

若存在唯一反函数

$$
x=x(u,v),\qquad y=y(u,v),
$$

且偏导连续，则

$$
f_{U,V}(u,v)=f_{X,Y}(x(u,v),y(u,v))
\left|
\frac{\partial(x,y)}{\partial(u,v)}
\right|.
$$

线性变换 $U=X+Y,V=X-Y$ 主要看 Jacobian。

令

$$
U=X+Y,\qquad V=X-Y
$$

则反解为

$$
x=\frac{u+v}{2},\qquad y=\frac{u-v}{2}
$$

Jacobian 绝对值为

$$
\left|
\frac{\partial(x,y)}{\partial(u,v)}
\right|=\frac{1}{2}
$$

所以联合密度变换时要乘上 $\frac{1}{2}$ 。

乘积变量 $U=XY$ 可以用变量变换公式算。

若要求 $U=XY$ 的密度，可以加一个辅助变量 $V=Y$
于是

$$
x=\frac{u}{v},\qquad y=v
$$

Jacobian 为

$$
\left|
\frac{\partial(x,y)}{\partial(u,v)}
\right|=\frac{1}{|v|}
$$

先得到 $(U,V)$ 的联合密度，再对 $v$ 积分得到 $U$ 的边际密度。

## 多维高斯分布

多维高斯只是把二维高斯写成矩阵形式。均值变成向量，方差变成协方差矩阵，指数里的平方项变成二次型。

对随机向量

$$
X=(X_1,X_2,\ldots,X_n)^\top,
$$

定义数学期望向量

$$
E(X)=(E(X_1),E(X_2),\ldots,E(X_n))^\top,
$$

以及协方差矩阵

$$
\mathrm{Cov}(X)=E((X-E(X))(X-E(X))^\top).
$$

协方差矩阵总是对称半正定的。

若 $X\sim N(\mu,B)$ ，其中 $B$ 正定，则密度为

$$
f(x)=\frac{1}{(2\pi)^{n/2}\det(B)^{1/2}}
\exp\left(-\frac{1}{2}(x-\mu)^\top B^{-1}(x-\mu)\right).
$$

若 $Z\sim N(0,I_n)$ ，且 $A$ 行满秩，则

$$
AZ+b\sim N(b,AA^\top).
$$

更一般地，若 $X\sim N(\mu,B)$ ，则

$$
AX+b\sim N(A\mu+b,ABA^\top).
$$

### 标准化与白化

这部分是后面很多证明的底层工具，标准高斯经过线性变换仍是高斯，一般高斯也可以反过来白化成标准高斯。

若 $X\sim N(\mu,B)$ ，可以写作

$$
X=B^{1/2}Z+\mu,\qquad Z\sim N(0,I_n).
$$

反过来

$$
Z=B^{-1/2}(X-\mu)
$$

称为白化。

标准高斯具有旋转不变性，若 $Q$ 为正交矩阵，且 $Z\sim N(0,I_n)$ ，则

$$
QZ\sim N(0,I_n).
$$

几何上，标准高斯的等密度面是球面，线性变换 $A$ 会把球面变成由 $AA^\top$ 刻画的椭球。若 $A=U\Sigma V^\top$ 为奇异值分解，则

$$
AA^\top=U\Sigma^2U^\top.
$$

这里 $\Sigma$ 控制椭球轴长， $U$ 控制椭球方向， $\det(AA^\top)^{1/2}$ 控制体积缩放。
