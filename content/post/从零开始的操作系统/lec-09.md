---
title: "Lecture 09: Scheduling 1 - Concepts and Classic Policies"
slug: os-lec-09
date: 2026-06-22
seriesOrder: 9
encrypt: false
hidden: true
---

## 调度模型

### 调度问题

![Scheduling queues](assets/lecture-09/slide-008-scheduling-queues.png)

调度器的基本动作可以写成：

```c
run_new_thread() {
    if (readyThreads(TCBs)) {
        nextTCB = selectThread(TCBs);
        run(nextTCB);
    } else {
        run_idle_thread();
    }
}
```

分析调度策略时常假设每个程序只有一个用户、每个进程只有一个线程，并且进程之间独立。现实系统还要决定公平应落在用户、进程还是线程上，也要区分进程切换与线程切换的成本。

程序也不是一直占着 CPU。大多数 workload 在 CPU burst 和 I/O burst 之间交替：计算一段，等待 I/O，再计算一段。每次调度，本质上是在决定下一段 CPU 时间给哪个 runnable task。如果策略偏好短 CPU burst，通常会改善交互响应，因为 I/O-bound 或交互任务能更快运行一点点，然后继续等待外部事件。

### 调度指标

![Scheduling goals](assets/lecture-09/slide-011-scheduling-goals.png)

常见指标可以先分成几类：

| 指标 | 含义 |
| --- | --- |
| Completion/Turnaround time | 从任务到达到完成经过多久 |
| Waiting time | 在 ready queue 中等待 CPU 的总时间 |
| Response time | 从到达到第一次运行经过多久 |
| Throughput | 单位时间完成多少任务 |
| Fairness | CPU 时间如何在用户或任务之间共享 |

在确定性 workload 中，可以先画时间线，再填每个 job 的完成时刻、首次运行时刻和等待区间：

```text
turnaround_time = finish_time - arrival_time
waiting_time = turnaround_time - total_CPU_burst_time
response_time = first_run_time - arrival_time
throughput = completed_jobs / elapsed_time
```

这些指标不总是同向变化。减少平均完成时间可能偏向短任务，牺牲长任务公平；提高吞吐可能减少上下文切换，却让交互任务等得更久；追求等待时间公平，也可能让平均完成时间变差。因此调度策略的讨论，通常都是在说明自己愿意牺牲什么来换取什么。

## 经典策略

### FCFS

First Come, First Serve 按到达顺序运行任务：

```c
while (!ready_queue.empty()) {
    job = ready_queue.pop_front();
    run_until_block_or_finish(job);
}
```

它的优点是简单、开销低，也容易解释。问题是 head-of-line blocking：一个短任务如果排在长任务后面，会被长时间挡住。若所有任务长度相同，FCFS 不差；但任务长度差异越大，队头长任务造成的平均完成时间损失越明显。

FCFS 也提示我们：非抢占式调度器依赖任务主动阻塞或结束。如果一个任务一直不让出 CPU，后面的任务就没有进展机会。

### Round Robin

![RR quantum](assets/lecture-09/slide-015-rr-quantum.png)

![Quantum comparison](assets/lecture-09/slide-024-quantum-comparison.png)

Round Robin 给每个任务一个最多连续运行 `q` 的时间片，用完就被 timer interrupt 抢占并放回队尾：

```c
while (!ready_queue.empty()) {
    job = ready_queue.pop_front();
    run_for_at_most(job, quantum);

    if (!job.finished && !job.blocked) {
        ready_queue.push_back(job);
    }
}
```

如果 ready queue 中有 `n` 个任务，每个任务近似不会等超过 `(n - 1)q` 就再次运行。这让 RR 很适合改善交互响应和等待时间公平。但它并不保证 average completion time 总优于 FCFS。若短任务本来排在前面，FCFS 已经能让它们快速完成；RR 反而可能把短任务切碎，让完成时间变晚。

时间片选择直接影响 RR 的表现。`q` 无限大时，RR 退化成 FCFS；`q` 太大时，交互任务等待时间变差；`q` 太小时，上下文切换、cache/TLB 扰动和调度开销会吞掉吞吐。即使显式 context switch cost 为 0，频繁轮转也可能破坏 cache locality，让总运行时间变长。常见时间片在 10ms 到 100ms 之间，具体分析仍以系统参数为准。

### Priority Scheduling

Priority scheduling 给每个 job 一个优先级，调度器总是先运行最高优先级的 runnable task。Strict priority 的规则很清楚：只要高优先级队列非空，低优先级任务就不运行。因此它能表达重要性，也天然带来低优先级 starvation 风险。

为了公平，系统可以给低优先级队列保留 CPU 份额，或对长时间没得到服务的任务做 aging。代价是平均完成时间和高优先级响应可能变差。公平不是调度策略的附属品，而是目标函数的一部分。

Priority inversion 是另一个工程风险。典型三线程场景是：低优先级线程 L 先拿到锁；高优先级线程 H 后来需要这把锁，只能等待 L；中优先级线程 M 不需要锁，却不断抢占 L，导致 L 无法释放锁，H 被间接卡住。常见修复是 priority inheritance 或 donation：临时把持锁的 L 提升到 H 的优先级，让它尽快运行并释放锁。

### SJF / SRTF

![SJF SRTF](assets/lecture-09/slide-028-sjf-srtf.png)

Shortest Job First 在非抢占场景下选择总计算量最短的 job；Shortest Remaining Time First 是抢占式版本，选择剩余时间最短的 job，新来的短任务可以抢占当前长任务。

```c
// non-preemptive SJF
job = argmin(ready_queue, job.total_burst_time);
run_until_block_or_finish(job);

// preemptive SRTF
on_job_arrival_or_timer_interrupt() {
    job = argmin(ready_queue, job.remaining_time);
    run(job);
}
```

让短任务尽快离开系统，可以减少它们被长任务挡住的等待时间。在确定任务长度的模型中，SJF 最小化非抢占场景的 average completion time，SRTF 最小化抢占场景的 average completion time。如果所有 job 长度相同，SJF/SRTF 与 FCFS 差别不大；长度差异越大，SRTF 越能避免 head-of-line blocking。

现实问题是未来不可知。系统通常不知道 job 总长度或下一段 CPU burst，只能用历史估计、用户提示或后续的 MLFQ 之类反馈策略近似。另一个代价是长任务可能被源源不断的短任务推迟，产生 starvation。
