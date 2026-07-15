---
title: 分布式训练与数据并行
date: 2025-12-03
categories:
    - AI
slug: ai-programming-distributed-data-parallel
hidden: true
seriesOrder: 16
---

## 训练规模

训练规模同时受计算量和内存限制。模型放得进一张卡，也可能要花数月才能完成训练；增加参数、上下文长度与 batch 后，权重、梯度、优化器状态和 activation 又可能直接超过单卡显存。多设备既能缩短同一任务的训练时间，也能容纳单机放不下的模型。

分布式系统由多台通过网络连接的计算机共同完成任务。它提供了更多算力和内存，也带来了通信延迟、节点故障、时钟差异与状态一致性问题。训练框架需要把这些问题收进 process group、collective 和 checkpoint 等抽象中，模型代码才不必直接处理每一次网络收发。

## 运行环境

训练扩展到多个 device 与节点后，每张 GPU 只能直接访问本地内存，节点之间还隔着带宽和延迟不同的互连。进程、rank 与通信拓扑共同组成实际执行环境。

![分布式训练的硬件层次](assets/slides/16-hardware-overview.png)

扩展并不会自动带来线性加速。节点越多，计算被切得越细，通信、同步和负载不均衡所占比例越大。Amdahl's Law 表明无法并行的部分会限制最终 speedup。

分布式程序通常让每张 GPU 对应一个进程。每个进程有唯一的 rank，参与训练的进程总数称为 world size。多个 rank 先组成 process group，collective communication 只在这个 group 内发生。

```python
import os

import torch


torch.distributed.init_process_group(backend="nccl")

local_rank = int(os.environ["LOCAL_RANK"])
torch.cuda.set_device(local_rank)

model = model.to(local_rank)
model = torch.nn.parallel.DistributedDataParallel(
    model,
    device_ids=[local_rank],
)
```

一机四卡时，rank 常取 $0$ 到 $3$ 这四个值，每个进程只控制自己的 GPU。多机训练还需要把全局 rank 映射到节点和本地设备，不能把 global rank 直接当作本机 CUDA id。

### 通信层次

同一系统内的传输路径可以分成几层：

- 同一 GPU 内由 register、shared memory 和 global memory 连接 thread。
- 节点内 GPU 之间经过 PCIe、NVLink 或 NVSwitch。
- 节点间通过 Ethernet、InfiniBand、RoCE 与 RDMA。
- 远程存储还会占用独立或共享的网络链路。

通信时间常用简单模型表示

$$
T(n)=\alpha+\beta n
$$

$\alpha$ 是每次通信的固定启动延迟， $\beta$ 是每 byte 的传输成本， $n$ 是消息大小。小消息主要受 latency 限制，大消息主要受 bandwidth 限制。把许多小 Tensor 合并成 bucket，可以减少重复支付 $\alpha$ 的次数。

### 集合通信

Collective 由一组 rank 共同参与。所有 rank 必须以一致的顺序进入相同 collective，否则程序会永久等待或直接报错。

![常见 Collective](assets/slides/16-collectives.png)

- Broadcast 把一个 rank 的数据复制给所有 rank。
- Scatter 把一份数据切成若干块并分发。
- Gather 收集各 rank 的分片到一个 rank。
- AllGather 让所有 rank 都得到全部分片。
- Reduce 聚合所有 rank 的数据到一个 rank。
- AllReduce 聚合后把结果发给所有 rank。
- ReduceScatter 聚合并把结果分片留在各 rank。
- AllToAll 让每个 rank 分别向所有 rank 发送一个分片。

Reduce 的运算可以是 sum、max、min 或其他满足要求的结合操作。浮点加法不严格满足结合律，通信树和 rank 数改变后，低位结果可能略有差异。

MapReduce 把数据处理拆成 Map、Shuffle 与 Reduce。Map 将输入记录变成键值对，Shuffle 把同 key 的值送到同一个 Reduce，Reduce 再完成聚合。

这种执行方式允许中间结果落盘，也容易在任务失败后单独重算某个 partition，因此很适合日志统计和离线数据处理。神经网络训练的参数却会在每个 step 后改变，下一步必须读取上一轮更新后的状态。若每次都经过落盘、Shuffle 和任务重新调度，通信延迟会远大于 GPU 计算时间。

分布式训练借用了数据分片与归约的思想，但把它们放进常驻进程和内存中的 collective。Rank 在整个训练期间保持存活，梯度一旦 ready 就能直接进入 AllReduce，也可以与后续 backward 重叠。二者的区别不在于有没有 Map 和 Reduce，而在于迭代状态是否常驻，以及通信路径是否为高频同步优化。

## 数据并行

Data Parallelism 在每个 rank 保存完整模型，把 mini-batch 按 rank 切分。rank $r$ 计算本地梯度

$$
g_r=\frac{1}{|B_r|}\sum_{x_i\in B_r}\nabla_\theta\ell(x_i;\theta)
$$

当各 rank 的 local batch size 相同时，随后对梯度执行 AllReduce 并取平均

$$
g=\frac{1}{P}\sum_{r=1}^{P}g_r
$$

所有 rank 使用相同 $g$ 更新相同参数，因此下一步仍保持一致。

![数据并行训练](assets/slides/16-data-parallel.png)

若每个 rank 的 local batch size 不变，world size 增大后 global batch size 也会增大。学习率、warmup、正则化和训练步数可能都要调整。若保持 global batch 不变，则每个 rank 的计算量变小，通信更难被摊薄。

Backward 从输出层向输入层逐步产生梯度。DistributedDataParallel 不必等所有梯度计算完再通信，而是把梯度按 bucket 组织；某个 bucket 中的梯度全部 ready 后，立即启动异步 AllReduce，与后续 backward 重叠。

Bucket 太小会产生大量小 collective，太大则推迟第一轮通信。参数在 backward 中的 ready 顺序与 bucket 顺序不匹配时，也会形成等待。

## 参数同步

### 同步与异步

Synchronous SGD 每一步等待所有 worker 完成梯度。参数版本一致，行为最接近单机大 batch；最慢 worker 会决定整步时间，straggler 因此很昂贵。

Asynchronous SGD 允许 worker 使用稍旧的参数计算并独立提交梯度。它减少全局等待，却引入 staleness：梯度对应的模型版本可能已经落后。异步程度过高时，收敛会变慢或不稳定。

实践中的 GPU 大模型训练通常使用同步 collective，再通过数据预取、通信重叠和故障恢复降低等待成本。

### 参数服务器

Parameter Server 架构把参数分片放在 server，worker 拉取参数、计算梯度并推送更新。

![Parameter Server](assets/slides/16-parameter-server.png)

一次训练 step 中，worker 先从对应 shard 拉取参数，在本地完成 forward 与 backward，再把梯度推回 server。同步模式会等这一批 worker 全部提交后统一更新；异步模式则在梯度到达时立即更新。Bounded staleness 介于两者之间，允许 worker 落后有限个版本，超过范围后再等待。

参数按 key 分片后，只有本批数据访问到的稀疏 embedding 才需要传输，因而 Parameter Server 很适合超大推荐模型。代价是热点 key 会集中访问少数 shard，server 的网卡、CPU 或锁竞争都可能成为瓶颈。系统通常还要复制热点参数、重新划分 shard，或先在节点内合并梯度再发往 server。

AllReduce 则让 worker 直接协作完成聚合，不保留中心 server。稠密梯度训练中，它通常能更充分地利用集群互连。

## AllReduce

### Tree 与 Ring

Tree 以 $O(\log P)$ 轮完成归约与广播，固定延迟较低，适合消息较小或层次化网络。树的上层链路需要承载更多聚合结果，拓扑不匹配时可能形成热点。

Ring AllReduce 分成 ReduceScatter 与 AllGather。每个 rank 把 Tensor 切成 $P$ 块，沿 ring 发送和聚合，之后再沿 ring 收集完整结果。

![Ring Reduction](assets/slides/16-ring-reduce.png)

设四个 rank 各有一份分成四块的梯度。ReduceScatter 的每一轮中，每个 rank 向右邻居发送一块，同时从左邻居接收一块并累加。三轮后，每个 rank 持有一块已经聚合完成的结果。AllGather 再传三轮，把四块结果传播给所有 rank。最终每个 rank 都得到同一份完整梯度。

每个 rank 传输的数据量接近

$$
2\frac{P-1}{P}N
$$

当消息很大时，ring 能接近链路带宽上限；它需要 $2(P-1)$ 个通信阶段，小消息则容易被阶段延迟拖慢。

Tree 用更少的通信阶段换取不均匀的链路负载，Ring 则让每条链路持续传输大小接近的分片。前者更适合小消息，后者更容易在大消息上吃满带宽。真实库会根据消息大小、rank 数和硬件拓扑在 ring、tree、CollNet 等算法间选择。多节点系统还可以先在节点内 ReduceScatter，再跨节点归约，最后回到节点内 AllGather。

### AllToAll

AllReduce 的每个 rank 最终得到相同结果，适合让所有数据并行副本保持一致。AllToAll 的目的不同：每个 rank 都把一块不同的数据发送给其他 rank，接收后得到按目标重新分组的分片。Mixture-of-Experts 的 token dispatch 就常使用 AllToAll，把 token 送到负责相应 expert 的设备。

![AllReduce 与 AllToAll](assets/slides/16-allreduce-alltoall.png)

设每个 rank 持有 $N$ 个 token，路由器先按 expert 归属把它们整理成 $P$ 份，再分别发往对应 rank。通信前后 Tensor 的总元素数没有变化，数据的归属却完全重排。它比 AllReduce 更依赖网络双向带宽、路由和负载均衡。Expert 分配不均时，即使总 token 数相同，最拥挤的 rank 仍会决定整体速度，实际系统常用 capacity limit 或 auxiliary loss 避免少数 expert 被挤满。

## 性能与容错

### 性能

单步时间可以粗略拆成

$$
T_{step}=T_{input}+T_{forward}+T_{backward}+T_{communication}+T_{update}-T_{overlap}
$$

只增加 GPU 数而不改变模型和 global batch 时，单 rank 计算量下降，通信量却未必同步下降，scaling efficiency 会逐渐变差。

常见问题包括：

- DataLoader 让部分 rank 更晚进入 step。
- 不同输入长度造成计算不均衡。
- collective 顺序不一致或 bucket 过碎。
- 跨 NUMA、跨 PCIe root complex 或跨慢链路通信。
- 某个 rank 的频率、温度、网络重传或后台任务异常。
- 频繁读取 host scalar 导致隐式 device synchronization。

分析时要对齐各 rank 的 timeline。单看某一张 GPU 图，很容易把等待其他 rank 的空白误判成自身 kernel 性能不足。

### Checkpoint

同步训练中任一 rank 失效都会中断 collective。训练系统需要定期保存模型、optimizer、scheduler、scaler 与数据位置。大规模任务还会使用 sharded checkpoint，避免由单一 rank 汇总全部状态。

Elastic training 可以在节点退出后重新组成 process group，但 world size 改变会影响 batch size、sampler 和学习率语义。恢复点必须明确记录这些配置，不能只依赖权重文件。
