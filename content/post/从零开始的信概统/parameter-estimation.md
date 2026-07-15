---
title: 参数估计
date: 2026-01-02
categories:
    - 数学
slug: 参数估计
hidden: true
seriesOrder: 7
---

## 统计学的基本概念

除非另有说明，以下估计量都基于简单随机样本。

- 总体，研究对象的全体。
- 个体，总体中的一个成员。
- 样本，从总体中随机抽取的 $n$ 个个体，记作 $X_1,\ldots,X_n$ 。
- 样本量，样本个数 $n$ 。
- 简单随机样本， $X_1,\ldots,X_n$ 相互独立，且与总体 $X$ 同分布。

若总体分布函数为 $F(x)$ ，简单随机样本的联合分布函数为

$$
F(x_1,\ldots,x_n)=\prod_{i=1}^{n}F(x_i).
$$

统计量是不依赖未知参数的样本函数。常用统计量包括

$$
\bar{X}=\frac{1}{n}\sum_{i=1}^{n}X_i.
$$

样本方差常写为

$$
S^2=\frac{1}{n-1}\sum_{i=1}^{n}(X_i-\bar{X})^2.
$$

样本 $k$ 阶原点矩为

$$
A_k=\frac{1}{n}\sum_{i=1}^{n}X_i^k.
$$

样本 $k$ 阶中心矩为

$$
B_k=\frac{1}{n}\sum_{i=1}^{n}(X_i-\bar{X})^k.
$$

## 点估计

点估计用样本构造统计量来估计未知参数 $\theta$ 。由于样本具有随机性，估计量本身也是随机变量，记为

$$
\hat{\theta}=\hat{\theta}(X_1,\ldots,X_n).
$$

给定样本取值后， $\hat{\theta}(x_1,\ldots,x_n)$ 称为估计值。

## 估计量的评价

偏差衡量估计量均值与真实参数的距离，均方误差同时计入偏差和波动，一致性则描述样本量增大时的收敛。

估计量的偏差为

$$
\mathrm{Bias}(\hat{\theta})=E(\hat{\theta})-\theta.
$$

若 $\mathrm{Bias}(\hat{\theta})=0$ ，则称估计量无偏。若

$$
\lim_{n\to+\infty}E(\hat{\theta}_n)=\theta,
$$

则称估计量渐进无偏。

均方误差定义为

$$
\mathrm{MSE}(\hat{\theta})=E((\hat{\theta}-\theta)^2).
$$

它满足分解公式

$$
\mathrm{MSE}(\hat{\theta})
=\mathrm{Var}(\hat{\theta})+\mathrm{Bias}(\hat{\theta})^2.
$$

若估计量无偏，则均方误差等于方差。

若

$$
\hat{\theta}_n\xrightarrow{P}\theta,
$$

则称 $\hat{\theta}_n$ 是一致估计量。一个常用充分条件是

$$
\mathrm{MSE}(\hat{\theta}_n)\to 0.
$$

对 $(\hat{\theta}_n-\theta)^2$ 使用 Markov 不等式可得

$$
P(|\hat{\theta}_n-\theta|\geq \epsilon)
\leq
\frac{\mathrm{MSE}(\hat{\theta}_n)}{\epsilon^2}.
$$

这些性质之间没有直接的等价关系：

- 无偏估计量不一定一致。
- 有偏估计量也可能一致。
- 一致性直接描述估计量在大样本下的收敛。

## 样本均值与样本方差

样本方差的分母为 $n-1$ 。由于 $\bar{X}$ 也由同一组样本估计，中心化后的 $n$ 个偏差之和为零，因而损失一个自由度。

若总体期望和方差存在，则 $\bar{X}$ 是 $E(X)$ 的无偏估计量，并且

$$
\mathrm{MSE}(\bar{X})=\mathrm{Var}(\bar{X})=\frac{\mathrm{Var}(X)}{n}.
$$

样本二阶中心矩

$$
B_2=\frac{1}{n}\sum_{i=1}^{n}(X_i-\bar{X})^2
$$

不是 $\mathrm{Var}(X)$ 的无偏估计，因为

$$
E(B_2)=\frac{n-1}{n}\mathrm{Var}(X).
$$

因此

$$
S^2=\frac{n}{n-1}B_2=\frac{1}{n-1}\sum_{i=1}^{n}(X_i-\bar{X})^2
$$

是总体方差的无偏估计量。

## 矩法估计

矩法用样本矩替换总体矩。若未知参数 $\theta_1,\ldots,\theta_k$ 可以表示为总体前 $k$ 阶矩的函数

$$
\theta_i=f_i(\mu_1,\ldots,\mu_k),
$$

则用样本矩 $A_1,\ldots,A_k$ 替换总体矩，得到估计量

$$
\hat{\theta}_i=f_i(A_1,\ldots,A_k).
$$

例如若总体 $X\sim \mathrm{Exp}(\lambda)$ ，则

$$
E(X)=\frac{1}{\lambda}.
$$

用 $\bar{X}$ 替换 $E(X)$ ，得到矩估计

$$
\hat{\lambda}=\frac{1}{\bar{X}}.
$$

矩法通常计算简单，但未必是无偏估计或最优估计。

## 最大似然估计

给定样本 $x_1,\ldots,x_n$ ，似然函数为

$$
L(\theta)=P(X_1=x_1,\ldots,X_n=x_n;\theta)
$$

在连续情形中则使用联合密度。若样本为简单随机样本，则

$$
L(\theta)=\prod_{i=1}^{n}f(x_i;\theta).
$$

最大似然估计选择使 $L(\theta)$ 最大的参数。通常转化为最大化对数似然函数

$$
\ell(\theta)=\ln L(\theta)=\sum_{i=1}^{n}\ln f(x_i;\theta).
$$

最大似然估计具有不变性，若 $\hat{\theta}$ 是 $\theta$ 的最大似然估计，且 $g$ 单值可逆，则 $g(\theta)$ 的最大似然估计为 $g(\hat{\theta})$ 。

## 最大似然与交叉熵

分类模型中的 softmax + cross entropy 可以由最大似然直接导出。

分类模型给出条件分布 $f_\theta(y|x)$ 。给定训练数据 $(x_i,y_i)$ ，最大似然函数为

$$
L(\theta)=\prod_{i=1}^{n}f_\theta(y_i|x_i).
$$

最大化似然等价于最小化负对数似然

$$
-\ln L(\theta)=\sum_{i=1}^{n}-\ln f_\theta(y_i|x_i).
$$

若真实标签分布记为 $p(y|x_i)=\mathbf{1}_{y=y_i}$ ，则单个样本的交叉熵为

$$
H_i(p,f_\theta)=-\sum_y p(y|x_i)\ln f_\theta(y|x_i)=-\ln f_\theta(y_i|x_i).
$$

所以最大似然估计等价于最小化交叉熵损失。分类模型常用 softmax 把实数输出转成概率分布

$$
\mathrm{softmax}(a)_i=\frac{e^{a_i}}{\sum_j e^{a_j}}.
$$

## 区间估计

区间估计构造统计量 $\hat{\theta}_L$ 与 $\hat{\theta}_U$ ，使未知参数以较高概率落入区间

$$
P(\hat{\theta}_L\leq \theta\leq \hat{\theta}_U)\geq 1-\alpha.
$$

此时 $[\hat{\theta}_L,\hat{\theta}_U]$ 称为置信水平为 $1-\alpha$ 的置信区间。

单侧置信下限满足

$$
P(\hat{\theta}_L\leq \theta)\geq 1-\alpha.
$$

单侧置信上限满足

$$
P(\theta\leq \hat{\theta}_U)\geq 1-\alpha.
$$

若一个下限置信水平为 $1-\alpha_1$ ，一个上限置信水平为 $1-\alpha_2$ ，则合成区间的置信水平至少为

$$
1-\alpha_1-\alpha_2.
$$

## 枢轴量法

枢轴量是分布不含未知参数的统计量。利用它构造置信区间可以分为三步

1. 找到统计量 $G=G(X_1,\ldots,X_n,\theta)$ ，使 $G$ 的分布不含未知参数。
2. 选择常数 $c,d$ ，使得 $P(c\leq G\leq d)=1-\alpha$ 。
3. 将 $c\leq G\leq d$ 改写为 $\hat{\theta}_L\leq \theta\leq \hat{\theta}_U$ 。

通常从点估计量出发构造枢轴量。

## 典型置信区间

### 正态总体均值，方差已知

若 $X\sim N(\mu,\sigma^2)$ ，且 $\sigma^2$ 已知，则

$$
\bar{X}\sim N\left(\mu,\frac{\sigma^2}{n}\right).
$$

于是

$$
\frac{\bar{X}-\mu}{\sigma/\sqrt{n}}\sim N(0,1).
$$

令 $\Phi$ 为标准正态分布函数，取

$$
z_{\alpha/2}=\Phi^{-1}(1-\alpha/2).
$$

则

$$
P\left(
\bar{X}-z_{\alpha/2}\frac{\sigma}{\sqrt{n}}
\leq
\mu
\leq
\bar{X}+z_{\alpha/2}\frac{\sigma}{\sqrt{n}}
\right)=1-\alpha.
$$

也可以用尾不等式给出更粗但分布无关的区间。例如正态尾界给出

$$
P\left(
\left|\bar{X}-\mu\right|
\leq
\frac{\sigma\sqrt{2\ln(2/\alpha)}}{\sqrt{n}}
\right)\geq 1-\alpha.
$$

### 均匀分布上界

若 $X\sim U(0,\theta)$ ，令

$$
\hat{\theta}=\max\lbrace X_1,\ldots,X_n\rbrace.
$$

则对 $0\leq x\leq \theta$ 有

$$
P(\hat{\theta}\leq x)=\left(\frac{x}{\theta}\right)^n.
$$

取枢轴量

$$
G=\frac{\hat{\theta}}{\theta}.
$$

则 $P(G\leq g)=g^n$ 。取 $c=\alpha^{1/n}$ ， $d=1$ ，得到

$$
P(\alpha^{1/n}\leq \hat{\theta}/\theta\leq 1)=1-\alpha.
$$

等价地

$$
P\left(\hat{\theta}\leq \theta\leq \alpha^{-1/n}\hat{\theta}\right)=1-\alpha.
$$

### 正态总体方差

若 $X\sim N(\mu,\sigma^2)$ ，则

$$
\frac{(n-1)S^2}{\sigma^2}\sim \chi^2(n-1).
$$

令 $F$ 为 $\chi^2(n-1)$ 分布函数，取

$$
c=F^{-1}(\alpha/2),\qquad d=F^{-1}(1-\alpha/2).
$$

则

$$
P\left(
\frac{(n-1)S^2}{d}
\leq
\sigma^2
\leq
\frac{(n-1)S^2}{c}
\right)=1-\alpha.
$$

### 伯努利参数

若 $X\sim B(1,p)$ ，样本均值 $\bar{X}$ 是 $p$ 的无偏估计。由 Chernoff-Hoeffding

$$
P(|\bar{X}-p| \gt \epsilon)\leq 2e^{-2n\epsilon^2}.
$$

令 $2e^{-2n\epsilon^2}=\alpha$ ，得

$$
\epsilon=\sqrt{\frac{\ln(2/\alpha)}{2n}}.
$$

因此

$$
P\left(
\bar{X}-\sqrt{\frac{\ln(2/\alpha)}{2n}}
\leq
p
\leq
\bar{X}+\sqrt{\frac{\ln(2/\alpha)}{2n}}
\right)\geq 1-\alpha.
$$

也可以用中心极限定理构造近似置信区间。

## 游戏机采样应用

游戏机采样是一个带未知 Bernoulli 参数的选择问题，目标是在有限样本下找到中奖概率接近最优的游戏机。

有 $n$ 台游戏机，第 $i$ 台中奖概率为未知参数 $p_i$ 。每次可以选择一台游戏机并观察一次 Bernoulli 结果。目标是返回一台游戏机 $o$ ，使

$$
P\left(p_o\geq \max_i p_i-\epsilon\right)\geq \frac{2}{3}.
$$

对每台游戏机取相同样本数：

1. 对每台游戏机采集 $N$ 次样本。
2. 计算每台游戏机的样本均值 $\bar{X}_i$ 。
3. 返回样本均值最大的游戏机。

对固定 $i$ ，若

$$
N=O\left(\frac{\ln(1/\alpha)}{\epsilon^2}\right),
$$

则

$$
P(|\bar{X}_i-p_i|\leq \epsilon)\geq 1-\alpha.
$$

对全部 $i$ 使用 Union Bound，取 $\alpha=\frac{1}{3n}$ ，可得

$$
P(\forall i,\ |\bar{X}_i-p_i|\leq \epsilon)\geq \frac{2}{3}.
$$

此时返回的 $o$ 满足

$$
p_o\geq \max_i p_i-2\epsilon.
$$

若要误差写成 $\epsilon$ ，只需把每台的估计误差控制在 $\epsilon/2$ ，样本量仍为

$$
N=O\left(\frac{\ln n}{\epsilon^2}\right).
$$

更一般地，若要求成功概率至少 $1-\delta$ ，则取

$$
N=O\left(\frac{\ln(n/\delta)}{\epsilon^2}\right).
$$
