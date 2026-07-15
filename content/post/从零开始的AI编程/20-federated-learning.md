---
title: 联邦学习
date: 2025-12-18
categories:
    - AI
slug: ai-programming-federated-learning
hidden: true
seriesOrder: 20
---

## 联邦场景

把所有数据集中到数据中心最容易训练，却可能卡在隐私、法规、上传成本和数据所有权上。让每个机构或设备独立训练也不理想。单个参与方的数据通常更少，覆盖的用户和标签也更窄，模型很容易只适应本地分布。

Federated Learning 让参与方共享训练结果，而不直接共享原始样本。典型参与方包括移动设备、医疗机构与企业。Server 把模型发送到数据所在位置，client 在本地训练后再上传模型更新。Gradient 和 parameter update 仍可能泄露样本信息，因此原始数据没有离开设备并不等于训练过程天然安全，server、client 与通信链路仍要放进同一套威胁模型中考虑。

联邦学习常见的两类场景是 cross-device 和 cross-silo。

![Cross-device 与 Cross-silo](assets/slides/20-cross-device-silo.png)

Cross-device FL 面向大量手机或边缘设备。每轮只抽取少量在线 client，设备算力、网络和电量差异很大，也可能随时掉线。

Cross-silo FL 面向少量组织或数据中心。参与方较稳定，单方数据量和算力更大，通常要求更严格的访问控制、审计与组织间协议。

![两类联邦学习的比较](assets/slides/20-comparison.png)

分布式训练默认各 worker 由同一主体管理，数据划分相对可控；联邦学习的 client 属于不同故障域和信任域，数据分布也通常高度 non-IID。

## FedAvg

一轮联邦训练包含几步：

1. Server 从可用 client 中采样一组参与者。
2. Server 下发当前全局模型和训练配置。
3. Client 在本地数据上执行若干 step 或 epoch。
4. Client 上传模型差值、梯度或其他更新。
5. Server 聚合更新并产生下一轮模型。

![联邦学习流程](assets/slides/20-federated-workflow.png)

Client selection 会影响统计偏差。总是选择网络快、充电中或高端设备，模型可能长期忽略另一部分用户分布。系统可用性与数据代表性需要一起考虑。

设全局参数为 $w_t = 1$ 。Client 1、Client 2 和 Client 3 分别拥有 $100$ 、 $300$ 和 $600$ 个样本，本地更新依次为 $\Delta w_1 = -0.2$ 、 $\Delta w_2 = 0.1$ 和 $\Delta w_3 = 0.05$ 。按样本数加权后

$$
\Delta w =
0.1\times(-0.2)
+
0.3\times0.1
+
0.6\times0.05 =
0.04
$$

Server 将全局参数更新为 $w_{t+1} = 1.04$ ，并把新参数发给下一轮 client。完整模型执行同样的加权，只是 $\Delta w_k$ 由标量变为参数向量。

设第 $k$ 个 client 有 $n_k$ 个样本，本地训练后得到参数 $w_{t+1}^{(k)}$ 。FedAvg 按样本数加权聚合

$$
w_{t+1}=\sum_{k\in S_t}\frac{n_k}{\sum_{j\in S_t}n_j}w_{t+1}^{(k)}
$$

![FedAvg](assets/slides/20-fedavg.png)

每个 client 从全局参数 $w_t$ 出发执行多步 local SGD。增加 local step 可以减少通信轮数，却会让各 client 沿自身数据分布走得更远。

![FedAvg 与集中式 SGD](assets/slides/20-fedavg-sgd.png)

当所有 client 数据近似 IID、每轮参与充分且 local step 较少时，FedAvg 接近大 batch 的分布式 SGD。non-IID 数据下，不同 client 的局部最优方向可能差异很大，简单平均会出现 client drift。

## 异质性

系统异质性来自设备算力、内存、网络、电量和在线时间差异。设置严格 deadline 会丢弃慢 client，等待全部 client 又会让 straggler 主导一轮时间。

统计异质性来自每个 client 的样本量、标签比例、语言、地区和采集方式不同。常见情形包括：

- 一个 client 只含少数类别。
- 不同 client 的特征分布不同。
- 标签规则或噪声水平不同。
- 数据量相差几个数量级。
- 分布随时间发生变化。

本地 loss 下降并不保证全局目标同步下降。除了训练平均模型，还要观察不同 client 群体上的 accuracy、worst-group performance 与收敛速度。

### FedProx

FedProx 在 client 本地目标中增加与全局参数的 proximal term

$$
\min_w F_k(w)+\frac{\mu}{2}\lVert w-w_t\rVert_2^2
$$

![FedProx](assets/slides/20-fedprox.png)

它限制本地参数偏离 $w_t$ 过远，缓解 non-IID 数据和不同本地计算量造成的 client drift。 $\mu$ 太大时，本地更新几乎无法利用 client 数据；太小时则退化为普通 FedAvg。

FedProx 不能消除全部异质性。Server momentum、control variate、adaptive aggregation 和不同 client 的动态 local step 还可以从其他方向改善稳定性。

### 个性化

单个全局模型未必同时适合所有 client。Personalized FL 可以共享 backbone，只在本地保存 head；也可以先训练全局模型，再用本地数据 fine-tune。

另一类方法把每个 client 的参数写成全局部分与个性部分的组合，并用正则项约束它们不要相差过远。相似 client 还可以聚类，共享组内模型。

Federated Multi-Task Learning 为每个 client 保留一组参数，再用任务关系矩阵约束相似 client 的模型靠近。它可以表达多个群体之间的关联，但需要额外估计任务关系，参与方数量很大时开销也会迅速增加。

Ditto 先用 FedAvg 等方法维护全局模型 $w$ 并让 client $k$ 另外优化个性化参数 $v_k$ 。本地目标为

$$
\min_{v_k} F_k(v_k)+\frac{\lambda}{2}\lVert v_k-w\rVert_2^2
$$

$\lambda$ 较大时，个性化模型更接近全局模型；较小时，它可以更多地适应本地数据。全局模型继续用于协作训练和新 client 初始化，本地模型则负责实际预测。

个性化模型更贴近本地分布，却增加模型版本、评估和部署复杂度。只在参与训练的 client 上报告结果，也可能高估对新 client 的泛化。

## 公平与安全

按样本数加权优化的是总体平均损失，数据多的 client 影响更大。少数 client 即使表现很差，也可能对平均指标影响很小。

![联邦学习中的公平性](assets/slides/20-fairness.png)

公平目标可以提高高损失 client 的权重、优化分位数或最坏组风险，也可以约束不同群体的性能差距。提高最差 client 表现可能降低总体平均精度，目标应由应用要求决定，不能只替换一个聚合公式就宣称公平。

系统公平同样重要。老旧设备若总因 deadline 被排除，对应用户的数据也不会影响模型。

![联邦学习的威胁模型](assets/slides/20-threat-model.png)

参与方可能包括 server、client、聚合服务、模型开发者和网络观察者。需要分别考虑：

- Honest-but-curious server 遵循协议，却尝试从 update 推断本地数据。
- Malicious client 上传构造更新，执行 poisoning 或 backdoor attack。
- 外部攻击者窃听、篡改或重放通信。
- Collusion 让若干参与方合并信息，绕过单方隐私保证。

TLS 保护 in-transit 数据，磁盘加密保护 at-rest 数据，但 server 解密后仍能看到单个更新。要隐藏更新内容，还需要 secure aggregation、trusted execution environment 或更强的密码学协议。

## 隐私

### 安全聚合

Secure Aggregation 让 server 只能得到更新之和，不能看到单个 client update。一个基本思路是 client 两两生成相反 mask，所有更新求和后 mask 自动抵消。

![Secure Aggregation](assets/slides/20-secure-aggregation.png)

实际协议还要处理 client 在提交 mask 后掉线的情况。Secret sharing 可以让剩余参与者恢复需要取消的 mask，同时不暴露仍在线 client 的单独更新。

Secure Aggregation 保护 update 的可见性，不限制聚合结果本身泄露的信息，也不能自动阻止恶意 client 上传异常值。聚合前无法直接查看单个 update 后，robust aggregation 和异常检测还会更难实现。

### TEE

TEE 在硬件隔离区域中解密并聚合 update，外部系统只能看到 attestation 与输出。它通常比完全密码学方案更高效，也能执行复杂聚合逻辑。

参与训练前，client 先验证远程 attestation，确认 enclave 正在运行约定版本的聚合代码，再把加密 update 发给它。解密密钥只交给通过验证的 enclave，host 操作系统即使控制进程和磁盘，也不能直接读取其中的明文更新。与只支持求和的安全聚合相比，TEE 更容易实现裁剪、异常检查和自定义加权。

这份信任并没有消失，而是集中到了硬件、固件、attestation 服务和 enclave 代码。侧信道、回滚旧版本及供应链漏洞都可能破坏隔离保证。Enclave 内存通常也小于完整模型更新，分块聚合时要保证每块使用同一轮参与者和同一组权重，不能让 host 通过重排分块改变结果。

### 差分隐私

Differential Privacy 限制单个样本或单个 client 对输出分布的影响。Client-level DP 通常先裁剪每个 client update 的范数，再对聚合结果加入噪声。

Record-level DP 把相邻数据集定义为相差一条样本记录，保护的是同一 client 内的单个样本。User-level DP 把一个用户的全部记录视为一个整体，更符合跨设备联邦学习的隐私目标，也更难获得相同精度。后文的裁剪单位是完整 client update，因此对应 user-level DP。

设裁剪阈值为 $C$ ，更新 $u_k$ 变为

$$
\widetilde{u}_k=u_k\min\left(1,\frac{C}{\lVert u_k\rVert_2}\right)
$$

聚合后加入 Gaussian noise

$$
\widetilde{u}=\frac{1}{|S_t|}\left(\sum_{k\in S_t}\widetilde{u}_k+\mathcal{N}(0,\sigma^2C^2I)\right)
$$

![Differential Privacy](assets/slides/20-differential-privacy.png)

训练多轮会累计隐私损耗，需要 privacy accountant 跟踪最终 $(\varepsilon,\delta)$ 。裁剪过强会丢失有用更新，噪声过大则降低模型精度；参与 client 越多，平均后噪声相对影响通常越小。

Secure Aggregation 与 DP 可以组合：前者防止 server 看到单个 update，后者限制最终聚合结果泄露个体信息。两者解决的问题不同。

## 鲁棒性

恶意 client 可以放大 update、定向修改某类输入，或协同植入 backdoor。按范数裁剪、median、trimmed mean 和 anomaly detection 可以降低部分攻击影响，但在 non-IID 数据下，正常少数 client 的更新本来就可能看起来异常。

模型更新还应绑定 round、模型版本和 client 身份，防止重放旧 update。部署前需要在正常分布、少数群体和安全测试集上分别评估，不能只观察聚合 loss。

## 联邦通信

一轮训练先把全局模型发给参与的 client，再收回本地更新。若模型含有 $P$ 个参数，每个参数按 $b$ 字节传输，一名 client 单次上传或下载的原始数据量约为 $Pb$ 。一个包含十亿个 FP32 参数的模型，仅单向传输一次就接近 $4\ \mathrm{GB}$ 。移动设备的上行带宽通常远低于下行带宽，因此上传更新往往比下发模型更慢，也更容易受网络切换和设备离线影响。

Server 不会等待所有设备。每轮会先抽取一批在线 client，并设置提交期限；在期限内完成训练的更新进入聚合，迟到的结果则被丢弃或延后处理。期限太短时，网络慢、算力弱的设备长期无法参与，最终模型会偏向条件较好的用户；期限太长又会让少数 straggler 拖慢整轮训练。参与率不只是系统参数，也会改变实际参与训练的数据分布。

降低通信量有三种常见办法。量化用更少的 bit 表示更新，稀疏化只发送绝对值较大的部分，增加 local step 则让一次通信承担更多本地计算。前两种方法会产生压缩误差，可以把本轮没有发出的残差留到下一轮补偿；增加 local step 不损失传输精度，却可能让参数沿本地分布偏移得更远。压缩率、轮数和 client drift 需要放在一起调节，不能只看每轮发送了多少字节。

安全聚合还会改变通信协议。Client 除了模型更新，还要交换或提交用于抵消的 mask。若参与者在提交部分材料后掉线，server 必须在不暴露其他更新的前提下恢复缺失 mask；剩余人数不足时，这一轮只能放弃。量化和稀疏化也要与安全聚合使用的有限域表示兼容，否则压缩后的更新无法直接进入聚合协议。

每次下发都应带有 round 和模型版本，上传请求则需要 client 身份、版本号与幂等标识。这样即使网络重试，server 也不会把同一份更新累计两次，更不会把旧模型产生的结果混入新一轮。Server 的 checkpoint 至少保存全局模型、optimizer、client sampling seed、当前 round 和 privacy accountant；恢复后可以重新选择参与者，不应要求上一轮掉线的设备再次出现。

Cross-device 场景默认设备随时消失，协议围绕超时、重试和部分参与设计。Cross-silo 的参与方较少且稳定，更适合在聚合前确认各机构的模型版本，并用事务或审计日志记录一次更新是否已经提交。两类场景面对的是同一个训练目标，通信和恢复策略却不能照搬。
