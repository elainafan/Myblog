---
title: 回归分析
date: 2026-01-02
categories:
    - 数学
slug: 回归分析
hidden: true
seriesOrder: 8
---

回归分析就是参数估计在“变量关系”上的版本。这里不是估计一个分布的均值或方差，而是估计 $x$ 和 $y$ 之间的关系。最基础的模型就是一元线性回归。

## 问题设定

先固定最基础的一元模型。这里的 $x_i$ 当作已经给定的设计点，随机性主要放在误差项里。

给定数据

$$
(x_1,y_1),(x_2,y_2),\ldots,(x_n,y_n),
$$

一元线性回归模型假设

$$
y_i=\alpha+\beta x_i+\epsilon_i.
$$

其中 $\alpha,\beta$ 为未知参数， $\epsilon_i$ 为误差项。通常假设

$$
E(\epsilon_i)=0,\qquad \mathrm{Var}(\epsilon_i)=\sigma^2,
$$

并且 $\epsilon_i$ 相互独立。这里 $x_i$ 被视为可精确测量或可控制的确定值。

估计得到 $\hat{\alpha},\hat{\beta}$ 后，经验回归函数为

$$
\hat{y}=\hat{\alpha}+\hat{\beta}x.
$$

给定新输入 $x_0$ 时， $\hat{y}_0=\hat{\alpha}+\hat{\beta}x_0$ 是预测值或拟合值。

## 一元最小二乘估计

最小二乘法的目标很直接，找一条直线，让所有点到这条直线的竖直残差平方和最小。

定义残差平方和

$$
Q(\alpha,\beta)=\sum_{i=1}^{n}(y_i-\beta x_i-\alpha)^2.
$$

选择使 $Q$ 最小的 $\alpha,\beta$ ，得到最小二乘估计。正规方程为

$$
\frac{\partial Q}{\partial \beta}
=-2\sum_{i=1}^{n}x_i(y_i-\beta x_i-\alpha)=0,
$$

以及

$$
\frac{\partial Q}{\partial \alpha}
=-2\sum_{i=1}^{n}(y_i-\beta x_i-\alpha)=0.
$$

记

$$
\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i,\qquad
\bar{y}=\frac{1}{n}\sum_{i=1}^{n}y_i.
$$

再记

$$
s_{xx}=\sum_{i=1}^{n}(x_i-\bar{x})^2,\qquad
s_{xy}=\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y}).
$$

若 $x_i$ 不全相同，则 $s_{xx} \gt 0$ ，并且

$$
\hat{\beta}=\frac{s_{xy}}{s_{xx}},\qquad
\hat{\alpha}=\bar{y}-\hat{\beta}\bar{x}.
$$

等价写成

$$
\hat{\beta} =
\frac{\sum_i x_iy_i-\frac{1}{n}(\sum_i x_i)(\sum_i y_i)}
{\sum_i x_i^2-\frac{1}{n}(\sum_i x_i)^2}.
$$

## 最小二乘估计的统计性质

把模型代回估计量之后，可以看到估计误差全部来自噪声 $\epsilon_i$ 。这也是后面算无偏性和方差的入口。

在模型

$$
y_i=\alpha+\beta x_i+\epsilon_i
$$

代入后得到

$$
\hat{\beta} =
\beta+\sum_{i=1}^{n}\epsilon_i\frac{x_i-\bar{x}}{s_{xx}}.
$$

同时

$$
\hat{\alpha} =
\alpha+\sum_{i=1}^{n}\epsilon_i
\left(
\frac{1}{n}-\frac{(x_i-\bar{x})\bar{x}}{s_{xx}}
\right).
$$

因此

$$
E(\hat{\beta})=\beta,\qquad E(\hat{\alpha})=\alpha.
$$

也即 $\hat{\alpha}$ 与 $\hat{\beta}$ 都是无偏估计量。

方差为

$$
\mathrm{Var}(\hat{\beta})=\frac{\sigma^2}{s_{xx}}.
$$

以及

$$
\mathrm{Var}(\hat{\alpha}) =
\sigma^2\left(\frac{1}{n}+\frac{\bar{x}^2}{s_{xx}}\right).
$$

协方差为

$$
\mathrm{Cov}(\hat{\alpha},\hat{\beta}) =
-\sigma^2\frac{\bar{x}}{s_{xx}}.
$$

由于二者无偏，均方误差等于对应方差。

## 拟合值、残差与方差估计

拟合值是模型解释出的部分，残差是没有解释掉的部分。残差平方和还能反过来估计噪声方差。

拟合值为

$$
\hat{y}_i=\hat{\alpha}+\hat{\beta}x_i.
$$

残差为

$$
e_i=y_i-\hat{y}_i.
$$

残差平方和为

$$
\mathrm{SSE}=\sum_{i=1}^{n}(y_i-\hat{y}_i)^2.
$$

可以证明

$$
E(\mathrm{SSE})=(n-2)\sigma^2.
$$

因此

$$
s^2=\frac{1}{n-2}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2
$$

是 $\sigma^2$ 的无偏估计量。

## 正态误差下的最大似然

如果误差服从正态分布，最小二乘就有了最大似然解释。这一点很重要，最小二乘不只是几何上自然，也和概率模型相匹配。

若进一步假设

$$
\epsilon_i\sim N(0,\sigma^2)
$$

且相互独立，则似然函数为

$$
L(\alpha,\beta,\sigma^2) =
\prod_{i=1}^{n}
\frac{1}{\sqrt{2\pi}\sigma}
\exp\left(
-\frac{(y_i-\alpha-\beta x_i)^2}{2\sigma^2}
\right).
$$

对固定的 $\sigma^2$ ，最大化似然等价于最小化残差平方和，所以 $\alpha,\beta$ 的最大似然估计与最小二乘估计相同。

对 $\sigma^2$ 求最大似然估计得到

$$
\hat{\sigma}_{\mathrm{MLE}}^2 =
\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2.
$$

这是有偏估计量。无偏估计量是

$$
s^2=\frac{1}{n-2}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2.
$$

在正态误差假设下可以得到

$$
\hat{\beta}\sim N\left(\beta,\frac{\sigma^2}{s_{xx}}\right),
$$

以及

$$
\hat{\alpha}\sim N\left(\alpha,\sigma^2\left(\frac{1}{n}+\frac{\bar{x}^2}{s_{xx}}\right)\right).
$$

并且

$$
\frac{(n-2)s^2}{\sigma^2}\sim \chi^2(n-2).
$$

该统计量与 $\hat{\alpha},\hat{\beta}$ 相互独立。

## 新点估计与预测区间

这里要区分“估计平均响应”和“预测新的观测值”。后者还会多一个新噪声，所以预测区间会更宽。

给定新输入 $x_0$ ，均值响应为

$$
E(y_0)=\alpha+\beta x_0.
$$

它的点估计为

$$
\hat{y}_0=\hat{\alpha}+\hat{\beta}x_0.
$$

因为

$$
E(\hat{y}_0)=\alpha+\beta x_0,
$$

且

$$
\mathrm{Var}(\hat{y}_0) =
\sigma^2\left(
\frac{1}{n}+\frac{(x_0-\bar{x})^2}{s_{xx}}
\right),
$$

在正态误差假设下有

$$
\frac{\hat{y}_0-(\alpha+\beta x_0)}
{s\sqrt{\frac{1}{n}+\frac{(x_0-\bar{x})^2}{s_{xx}}}}
\sim t(n-2).
$$

于是均值响应 $\alpha+\beta x_0$ 的置信水平为 $1-\alpha_0$ 的置信区间为

$$
\hat{y}_0
\pm
t_{n-2,1-\alpha_0/2}\,
s\sqrt{\frac{1}{n}+\frac{(x_0-\bar{x})^2}{s_{xx}}}.
$$

如果要预测一个新的观测值 $y_0=\alpha+\beta x_0+\epsilon_0$ ，还需要加上新噪声的方差。因此预测区间为

$$
\hat{y}_0
\pm
t_{n-2,1-\alpha_0/2}\,
s\sqrt{1+\frac{1}{n}+\frac{(x_0-\bar{x})^2}{s_{xx}}}.
$$

## 平方和分解与确定系数

这一节最好从几何上理解，总波动可以拆成模型解释的部分和模型没解释掉的部分。

定义

$$
\mathrm{SST}=\sum_{i=1}^{n}(y_i-\bar{y})^2.
$$

$$
\mathrm{SSE}=\sum_{i=1}^{n}(y_i-\hat{y}_i)^2.
$$

$$
\mathrm{SSR}=\sum_{i=1}^{n}(\hat{y}_i-\bar{y})^2.
$$

最小二乘的正规方程推出残差与拟合值的中心化部分正交，因此

$$
\mathrm{SST}=\mathrm{SSE}+\mathrm{SSR}.
$$

确定系数定义为

$$
r^2=1-\frac{\mathrm{SSE}}{\mathrm{SST}} =
\frac{\mathrm{SSR}}{\mathrm{SST}}.
$$

它满足 $0\leq r^2\leq 1$ ，表示总平方和中可被回归模型解释的比例。

## 多元线性回归

多元线性回归只是把一个自变量换成多个自变量。写成矩阵以后，公式反而比一元情形更整齐。

多元线性回归模型为

$$
y_i=x_i^\top\beta+\epsilon_i.
$$

其中

$$
x_i=[1,x_{i,1},x_{i,2},\ldots,x_{i,k}]^\top\in \mathbb{R}^{k+1}.
$$

把所有样本写成矩阵形式

$$
y=X\beta+\epsilon.
$$

最小二乘目标为

$$
Q(\beta)=\|y-X\beta\|_2^2.
$$

正规方程为

$$
X^\top X\hat{\beta}=X^\top y.
$$

若 $X$ 列满秩，则

$$
\hat{\beta}=(X^\top X)^{-1}X^\top y.
$$

在 $E(\epsilon)=0$ ， $\mathrm{Cov}(\epsilon)=\sigma^2I$ 的假设下可以得到

$$
E(\hat{\beta})=\beta.
$$

并且

$$
\mathrm{Cov}(\hat{\beta})=\sigma^2(X^\top X)^{-1}.
$$

这与一元情形中的

$$
\mathrm{Var}(\hat{\beta})=\frac{\sigma^2}{s_{xx}}
$$

是一致的。

## 投影矩阵

Hat 矩阵 $H$ 是这章最关键的对象之一。它把观测向量 $y$ 投影到 $X$ 的列空间里，投影结果就是拟合值 $\hat{y}$ 。

拟合向量为

$$
\hat{y}=X\hat{\beta}=X(X^\top X)^{-1}X^\top y.
$$

定义 Hat 矩阵

$$
H=X(X^\top X)^{-1}X^\top.
$$

则

$$
\hat{y}=Hy.
$$

矩阵 $H$ 有以下性质

- $H$ 对称。
- $H^2=H$ 。
- $HX=X$ 。
- $\mathrm{tr}(H)=k+1$ 。

因此 $H$ 是到 $X$ 的列空间上的正交投影。残差向量为

$$
y-\hat{y}=(I-H)y=(I-H)\epsilon.
$$

于是

$$
E(\|y-\hat{y}\|_2^2)=\sigma^2\mathrm{tr}(I-H)=\sigma^2(n-k-1).
$$

因此

$$
s^2=\frac{1}{n-k-1}\|y-\hat{y}\|_2^2
$$

是 $\sigma^2$ 的无偏估计量。

## 正态误差下的多元回归

这里和一元回归完全平行，只是标量方差换成了矩阵形式。

若

$$
\epsilon\sim N(0,\sigma^2I),
$$

则

$$
\hat{\beta}\sim N(\beta,\sigma^2(X^\top X)^{-1}).
$$

同时

$$
\frac{(n-k-1)s^2}{\sigma^2}\sim \chi^2(n-k-1).
$$

并且 $s^2$ 与 $\hat{\beta}$ 相互独立。

给定新数据 $x_0$ ，均值响应 $x_0^\top\beta$ 的点估计为

$$
x_0^\top\hat{\beta}.
$$

其方差为

$$
\mathrm{Var}(x_0^\top\hat{\beta}) =
\sigma^2 x_0^\top(X^\top X)^{-1}x_0.
$$

几何上， $x_0^\top(X^\top X)^{-1}x_0$ 描述新数据点与已有设计矩阵所刻画椭球之间的不匹配程度。

## 岭回归

当 $X^\top X$ 不可逆或者非常病态时，普通最小二乘会不稳定。岭回归通过加一个 $\ell_2$ 正则项来稳住解。

当 $X$ 列不满秩或近似不满秩时， $X^\top X$ 可能不可逆或病态。岭回归在最小二乘目标上加入 $\ell_2$ 正则项

$$
Q_\lambda(\beta)=\|y-X\beta\|_2^2+\lambda\|\beta\|_2^2.
$$

求导得到

$$
(X^\top X+\lambda I)\hat{\beta}_\lambda=X^\top y.
$$

因此

$$
\hat{\beta}_\lambda=(X^\top X+\lambda I)^{-1}X^\top y.
$$

岭回归通常是有偏估计，因为

$$
E(\hat{\beta}_\lambda)
=(X^\top X+\lambda I)^{-1}X^\top X\beta =
\beta-\lambda(X^\top X+\lambda I)^{-1}\beta.
$$

它用偏差换取方差下降。协方差矩阵为

$$
\mathrm{Cov}(\hat{\beta}_\lambda) =
\sigma^2
(X^\top X+\lambda I)^{-1}X^\top X(X^\top X+\lambda I)^{-1}.
$$

## LASSO 与变量选择

岭回归倾向于把系数压小，LASSO 则更容易把一部分系数直接压成 $0$ ，所以它常用于变量选择。

多元回归中某些列可能是多余特征。直接枚举所有特征子集通常代价很高。LASSO 使用 $\ell_1$ 正则项

$$
Q_\lambda(\beta)=\|y-X\beta\|_2^2+\lambda\sum_i|\beta_i|.
$$

其中 $\lambda$ 为超参数，用于控制模型复杂度。与岭回归不同，LASSO 倾向于产生稀疏解，也就是把一些系数压到 $0$ ，因此常用于变量选择。
