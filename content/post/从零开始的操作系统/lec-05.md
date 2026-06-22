---
title: "Lecture 05: Synchronization 1: Concurrency"
slug: os-lec-05
date: 2026-06-22
seriesOrder: 5
encrypt: false
hidden: true
---

# Lecture 05: Synchronization 1: Concurrency

## 导读

OS 提供并发的第一步，是把进程和线程表示成可排队、可保存、可恢复的控制块。Context switch 也不是简单“跳到另一个线程”，而是先保存旧上下文，再恢复新上下文，让两个线程都能以为自己只是暂停了一下。

定时器中断让调度器能从不主动让出的线程手里夺回 CPU；同步机制则负责让共享可变状态在所有 interleaving 下都保持正确。后半讲用 tail latency 场景提醒我们：调度开销、队列不均衡和长请求阻塞短请求，都会被尾部延迟放大。

## 本讲地图

| 主题 | 解决的问题 | 关键结论 |
| --- | --- | --- |
| PCB/TCB | OS 如何表示可运行实体 | PCB 偏资源，TCB 偏执行上下文 |
| 生命周期 | 线程为什么在队列间移动 | ready/running/blocked 由调度、I/O、等待、抢占驱动 |
| Dispatch loop | 调度器如何推进系统 | run、choose、save、load 形成最小循环 |
| Context switch | 如何暂停并恢复线程 | 保存 PC/SP/寄存器，恢复新线程状态 |
| Timer interrupt | 线程不主动 yield 怎么办 | 外部中断强制回到内核调度路径 |
| Shared state | 为什么同步不可省 | 线程交错导致非确定性，需要锁、条件、信号量等约束 |

## 正文

线程真正跑起来之后，OS 要维护控制块、调度队列和切换路径。理解这些结构之后，context switch、抢占和 tail latency 就不是孤立概念了。

### 控制块

线程和进程没有运行时，并不是“消失”了。它们必须以某种形式留在内核里，等待下一次被调度、被唤醒或被终止。OS 提供并发的底层工作，就是维护这些实体的状态，并在合适时机把它们装回 CPU。

进程通常由 PCB 表示。PCB 记录进程状态、寄存器快照、PID、用户、可执行文件、优先级、执行时间、内存和 I/O 资源引用等。线程则需要 TCB，记录 PC、SP、寄存器、线程栈、线程状态等“下一条指令从哪继续”的信息。

可以粗略区分：

| 控制块 | 更关心什么 | 典型内容 |
| --- | --- | --- |
| PCB | 进程拥有什么资源 | 地址空间、文件表、权限、资源引用、进程级状态 |
| TCB | 线程如何继续执行 | PC、SP、寄存器、线程栈、线程状态 |

同一进程中的多个线程共享 PCB 指向的地址空间和全局资源，但每个线程必须有自己的 TCB 和 stack，否则它们无法独立暂停和恢复。

### 生命周期

![Thread lifecycle](assets/lecture-05/slide-012-thread-lifecycle.png)

生命周期图把 created、ready、running、waiting、terminated 这些状态串起来。

![Thread state](assets/lecture-05/slide-017-thread-state.png)

共享状态与 per-thread state 的分界，决定了同步和上下文切换各自关心什么。

进程或线程的生命周期可用几个状态描述。它们不是静态标签，而是调度器和等待事件共同推动的队列位置：

- new：正在创建。
- ready：已经可以运行，等待 CPU。
- running：指令正在执行。
- waiting / blocked：等待 I/O、锁、条件、join 等事件。
- terminated：执行结束。

调度本质上是队列管理。ready queue 里放可运行实体；不同设备、信号或条件可有不同等待队列。scheduler 决定从哪个队列、按什么策略取出下一个实体运行。

状态迁移可以按事件解释：

| 迁移 | 触发原因 |
| --- | --- |
| `created -> ready` | 控制块和初始资源建好，等待 CPU |
| `ready -> running` | scheduler 选中并 dispatch |
| `running -> blocked` | 发起 I/O、等待锁/条件、等待 join |
| `blocked -> ready` | I/O 完成、锁释放、signal/broadcast |
| `running -> ready` | timer interrupt 抢占，或主动 yield 后仍可运行 |

把这些迁移画清楚，后面分析同步、调度、I/O 阻塞和 server 并发模型都会更稳。

### Dispatch loop

![Context switch](assets/lecture-05/slide-023-context-switch.png)

Context switch 的核心是保存旧 TCB 状态并装载新 TCB 状态。

课程给出的调度循环可以抽象成：

```c
Loop {
    RunThread();
    ChooseNextThread();
    SaveStateOfCPU(curTCB);
    LoadStateOfCPU(newTCB);
}
```

`RunThread()` 会把线程状态装入 CPU，包括寄存器、PC、栈指针，以及必要的执行环境，例如地址空间。线程会一直运行，直到它阻塞、主动 yield、结束，或者被外部中断抢占。之后 OS 选择下一个 ready 线程，保存当前 CPU 状态，装载新线程状态。

线程切换通常比进程切换轻，因为同一进程内的线程共享地址空间，不需要切换完整内存映射。但它仍有成本：保存恢复寄存器、切换栈、进入退出内核路径、破坏缓存局部性，甚至影响 TLB。

### Context switch

Context switch 的代码骨架很朴素：

```c
Switch(tCur, tNew) {
    TCB[tCur].regs.r7 = CPU.r7;
    TCB[tCur].regs.r0 = CPU.r0;
    TCB[tCur].regs.sp = CPU.sp;
    TCB[tCur].regs.retpc = CPU.retpc;

    CPU.r7 = TCB[tNew].regs.r7;
    CPU.r0 = TCB[tNew].regs.r0;
    CPU.sp = TCB[tNew].regs.sp;
    CPU.retpc = TCB[tNew].regs.retpc;
    return;
}
```

真实系统要保存的状态更多，但原则相同：旧线程必须保存足够多的状态，才能以后从原位置继续；新线程必须恢复足够多的状态，才能像从未离开 CPU 一样继续。

如果切换代码漏保存某个寄存器，错误可能非常隐蔽。只有当被换下线程之后还依赖那个寄存器、并且某次 interleaving 恰好覆盖它时，程序才会输出错误结果。测试很难覆盖所有调度点和寄存器使用组合，所以 context switch 代码追求简单、通用、保守，而不是小聪明式优化。

Context switch 不是普通函数调用。它要保存旧线程寄存器、PC、栈指针等状态，再恢复新线程；旧线程会在未来某个时刻从保存点继续。

### 抢占控制

线程把控制权交回内核有两类路径：

- 内部事件：线程主动 `yield`、发起阻塞 I/O、等待锁/条件、等待其他线程信号。
- 外部事件：timer interrupt 等硬件中断强制打断当前线程。

如果只有内部事件，一个纯计算线程可能永远不主动让出 CPU。定时器中断解决了这个问题：硬件每隔一小段时间打断当前执行流，切到内核 handler，内核做 housekeeping，再决定是否调度其他线程。

`yield()` 通常会 trap 到 OS。内核从 ready queue 选出新线程，调用低层 switch 保存当前线程并恢复新线程。等旧线程以后重新被调度回来，它会从当初 trap/yield 返回路径继续执行，并做必要的 thread housekeeping。

新线程启动也需要预先布置 TCB 和栈：栈指针指向新栈顶，PC 或 return address 指向启动桩 `ThreadRoot`，参数寄存器放入用户函数指针和参数。`ThreadRoot` 做启动 bookkeeping，切到用户态，调用用户函数，结束后执行 `ThreadFinish` 唤醒 join 等待者并释放资源。

### 多核与 SMT

单核上并发来自时间复用，同一时刻只有一个线程的指令在执行。多核上多个线程可以真正并行运行。SMT / Hyperthreading 则在一个物理核心上暴露多个逻辑线程，让不同线程的指令填充执行单元空隙。

多核并行提升吞吐，但共享缓存、内存带宽和锁竞争会让加速不是线性的。SMT 的收益也不是线性，因为逻辑线程共享同一个物理核心的执行资源。OS 调度器把逻辑线程当成可调度 CPU，但性能判断必须记住底层资源仍然共享。

### Tail latency

![Shinjuku](assets/lecture-05/slide-049-shinjuku.png)

Shinjuku 展示了微秒级 tail latency 场景下快速抢占和专用调度的设计方向。

平均延迟好看不代表系统体验稳定。Tail latency 关注最慢的一小部分请求，例如 p99 或 p99.9。短请求如果排在长请求后面，会被队头阻塞拖高尾部。

微秒级系统里，普通 OS 的 interrupt、kernel crossing、scheduler 和 context switch 开销都可能太大。OS bypass、polling、run-to-completion 可以减少中断和调度开销，但如果长短任务混在一起，短请求仍可能被长请求占住核心。

Shinjuku 的方向是把快速抢占带回微秒级服务：专用 scheduling/queue core、硬件虚拟化支持快速抢占、用户态快速 context switch，并根据任务时长分布选择调度策略。它展示的不是“所有系统都该这么写”，而是尾延迟目标极端时，调度路径本身也要成为设计对象。

### 走向同步

![Bank server](assets/lecture-05/slide-054-bank-server.png)

ATM bank server 把共享数据库、并发请求和正确性约束放在同一个例子里。

ATM bank server 这样的例子说明了并发正确性的核心：服务器要同时处理多个请求，但不能破坏账户数据库，也不能多发钱。线程让每个请求像顺序程序一样写起来更自然，但多个请求共享数据库时就会出现 race。

并发程序必须面对 non-determinism：调度器能以任意顺序运行线程，也能在许多点切换。独立线程没有共享状态，结果通常更可复现；协作线程共享状态，就要保证所有 interleaving 都正确。

常见同步词汇可以这样组织：

| 概念 | 含义 |
| --- | --- |
| Synchronization | 线程之间围绕共享数据或事件进行协调 |
| Mutual exclusion | 同一时间只允许一个线程做某件事 |
| Critical section | 必须互斥执行的代码片段 |
| Lock | 提供 acquire/release 的互斥对象 |
| Semaphore | 非负整数同步对象，可做 mutex 或事件通知 |

多线程模型让每个请求可以“从头跑到尾”，业务代码接近顺序逻辑；代价是共享数据库、缓存、日志等都要同步。事件驱动模型减少线程数量和共享状态竞争，但把控制流拆成 callback 或状态机。工程上常见经验是先用正确的粗粒度锁打底，再根据热点和延迟目标细化。
