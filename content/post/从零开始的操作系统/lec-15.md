---
title: "Lecture 15: TLB/Cache Interaction and Demand Paging"
slug: os-lec-15
date: 2026-06-22
seriesOrder: 15
encrypt: false
hidden: true
---

## TLB 与 Cache

![Physically and virtually indexed caches](assets/lecture-15/slide-010-cache-indexing.png)

![Address translation path](assets/lecture-15/slide-016-address-translation.png)

### 问题

CPU 发出的是 virtual address，cache 最终要拿到数据。关键问题是 cache lookup 应该用 virtual address 还是 physical address。如果必须先完成地址翻译再查 cache，TLB 就进入 critical path；如果先用虚拟地址查 cache，又会引入别名和一致性问题。

### 机制

`Physically-indexed cache` 使用 physical address 查 cache。它的好处是同一份物理数据在 cache 中只有一个位置，context switch 后 cache 内容可以保留；代价是必须等 TLB 翻译出 PA，TLB lookup 会影响 cache 访问时间。

`Virtually-indexed cache` 使用 virtual address 查 cache，可能与 translation 并行甚至先于 translation。它的好处是更快；问题是同一个 physical page 可能被多个 virtual address 映射到 cache 的不同位置，形成 synonym/alias。context switch 后同名虚拟地址也可能指向不同物理页，因此可能需要 flush cache，或做更复杂的标记。

现代机器常通过 page offset 与 cache index 的位宽设计，让小 L1 cache 的部分 lookup 与 TLB lookup 重叠。

## TLB Organization

### 机制

TLB entry 通常包含：

| 字段 | 作用 |
| --- | --- |
| VPN | virtual page number |
| PPN | physical page number |
| protection bits | 读写执行、用户/内核等权限 |
| valid bit | entry 是否有效 |
| ASID/PID | 可选，用于区分不同地址空间 |

TLB 很小但必须很快，常见规模约 128-512 entries，现代机器可能更大。由于 TLB miss penalty 很高，TLB 不能有太多 conflict miss；小 TLB 常做成 fully associative。如果 fully associative 太慢，也可以在前面放一个很小的 direct-mapped TLB slice。

### 取舍

TLB miss 不等于 page fault。miss 只表示翻译缓存里没有，硬件或软件需要走 page table；只有 page table walk 后发现 PTE invalid 或权限不合法，才进入 page fault。

## TLB Consistency

### 问题

TLB 缓存的是 `VPN -> PPN`。context switch 后 address space 变了，同一个 VPN 可能属于另一个进程。如果继续使用旧 TLB entry，新进程可能错误访问旧进程的物理页。

### 机制

最简单的方法是 context switch 时 flush/invalidate TLB。这样做安全但昂贵，频繁切换时会让新进程经历一批冷 TLB miss。

更高效的方法是在 TLB entry 中加入 ASID/PID。硬件 lookup 时同时比较 VPN 和 ASID，不同进程的同名 VPN 可以共存。

TLB consistency 不只发生在 context switch。OS 修改 page table 时也必须 invalidate 对应 TLB entry。例如把某个页换出到 disk 后，如果旧 TLB entry 仍有效，硬件可能继续访问已经不该访问的 physical frame。

## Page Fault

page fault 是虚拟到物理翻译失败时发生的同步 fault/trap，与当前指令直接相关；它并非异步 interrupt。OS 修复后通常会重试原指令，因此处理前要先判断 fault 是否可修复。

可能原因包括：

| 原因 | 处理 |
| --- | --- |
| PTE marked invalid | 可能非法，也可能是 demand paging/COW/zero-fill |
| privilege level violation | 通常终止或报错 |
| access violation | 例如写 read-only page，可能是 COW，也可能非法 |
| PTE 不存在 | 可能是地址非法或页表需扩展 |
| page 不在内存 | demand paging 调入 |

保护违规通常直接终止进程；可修复 fault 则进入 OS handler，完成分配、调入或复制后再重试原指令。

## Demand Paging

demand paging 把 DRAM 作为 disk 的 cache。现代程序拥有很大的虚拟地址空间，但并非所有 code/data 都会同时活跃；常见的 90/10 rule 用来概括这种局部性。

两套术语的对应关系如下：

| Cache 术语 | Demand paging 对应物 |
| --- | --- |
| block size | 1 page，例如 4KB |
| organization | fully associative，因为虚拟页可放任意 physical frame |
| lookup | 先查 TLB，再 page table walk |
| miss | page fault，从 disk/backing store 取页 |
| replacement | FIFO/RANDOM/MIN/LRU/Clock 等 |
| write policy | write-back，需要 dirty bit |

write policy 必须接近 write-back。若每次写页都同步写 disk，代价不可接受；因此 dirty bit 用来判断 victim page 是否需要写回 backing store。

## Fault Handler

![Page fault to demand paging](assets/lecture-15/slide-021-page-fault.png)

page fault handler 的流程可以按“判断能否修复、准备 frame、读入目标页、恢复执行”来组织：

```text
1. CPU/MMU 发现 PTE invalid 或权限问题，trap 到 OS。
2. OS 判断 fault 是否可修复：
   - 非法访问：终止进程。
   - COW/stack growth/demand paging：继续处理。
3. 找一个 free frame；如果没有，选择 victim page。
4. 如果 victim dirty，写回 disk/backing store。
5. 将 victim 的 PTE 和相关 TLB entry 设为 invalid。
6. 从 disk/backing store 把目标页读入 frame。
7. 更新 faulting page 的 PTE：valid、PPN、权限、dirty/use 等。
8. 将 faulting thread 放回 ready queue，之后从原 faulting instruction 继续。
```

等待 disk I/O 时，faulting process/thread 进入 wait queue，OS 调度 ready queue 中的其他线程运行。Page fault 对当前指令是同步 fault，系统整体却不必空转等待。

## Backing Store

![Backing store](assets/lecture-15/slide-036-backing-store.png)

加载可执行文件时，OS 不必把整个 binary 读入内存。它可以先建立虚拟地址空间、page table 和文件/磁盘位置映射；代码页第一次被执行或访问时，再通过 page fault 加载。

VAS 的常见用途包括：

| 用途 | 机制 |
| --- | --- |
| stack growth | 访问 guard 区域后分配新页并 zero-fill |
| heap growth | 扩展地址空间并按需分配物理页 |
| fork | 复制 page table，COW 共享 parent pages |
| exec | 按需加载 binary |
| mmap | 把文件或 shared region 映射成内存 |

对于 non-resident page，OS 需要从 `(PID, page#)` 找到 disk block：

```text
FindBlock(PID, page#) -> disk_block
```

实现方式可能是利用 PTE spare bits 存 disk location，维护纯软件表，用连续 swap 区的紧凑表示，或用 hash table。

## Working Set Model

### 问题

程序执行时会在不同阶段访问不同页集合。`working set` 是进程最近一段时间实际访问的页集合。

### 机制

如果进程分到的 frames 足够容纳当前 working set，page fault rate 就低；如果 working set 放不下，进程会不断 fault，系统大量时间用于 paging，进入 thrashing。Working set 将 capacity miss、page frame allocation 与 thrashing 联系起来。

虚拟内存里一般不强调 conflict miss，因为 demand paging 可视为 fully associative cache：虚拟页可以放到任意 physical frame。更常见的是 compulsory miss、capacity miss，以及进程阶段切换导致的 working set 变化。

## Cost Model

![Effective access time](assets/lecture-15/slide-046-eat.png)

page fault penalty 比普通内存访问大很多，所以很小的 miss rate 也会让系统明显变慢。公式是：

```text
EAT = hit rate * hit time + miss rate * miss time
    = hit time + miss rate * miss penalty
```

若内存访问时间是 `200 ns`，page-fault service time 是 `8 ms = 8,000,000 ns`，page fault probability 是 `p`：

```text
EAT = 200 ns + p * 8,000,000 ns
```

如果每 1000 次访问有 1 次 page fault：

```text
p = 0.001
EAT = 200 + 8000 = 8200 ns = 8.2 us
```

这大约慢 40 倍。若希望 slowdown 小于 10%：

```text
EAT < 220 ns
p * 8,000,000 < 20
p < 2.5 * 10^-6
```

也就是约 400,000 次访问最多 1 次 page fault。这个数量级说明 demand paging 依赖强局部性；working set 一旦放不下，性能会迅速崩溃。
