---
title: 从零开始的操作系统
date: 2026-06-22
categories: 
    - 操作系统
    - 算法
seriesExclude: true
---

## 前言

这里用来存放《操作系统》课程的 Lecture 笔记。相比单篇总览，把每一讲拆开之后，之后补图、改正文、查某个主题都会舒服很多。

这一组笔记大致可以按五条线读：系统抽象、并发同步、调度、虚拟内存、I/O 与文件系统。读的时候不用急着把每个名词孤立背下来，更重要的是看清楚每一层抽象背后维护了哪些状态，以及这些状态在并发、故障和性能压力下会怎么变化。

## 阅读入口

### 系统抽象

- [Lecture 01: 操作系统的四个基本概念]({{< ref "lec-01.md" >}})
- [Lecture 02: Threads and Processes]({{< ref "lec-02.md" >}})
- [Lecture 03: Files and I/O]({{< ref "lec-03.md" >}})
- [Lecture 04: IPC, Pipes and Sockets]({{< ref "lec-04.md" >}})

### 并发同步

- [Lecture 05: Synchronization 1: Concurrency]({{< ref "lec-05.md" >}})
- [Lecture 06: Synchronization 2 - Semaphores and Bounded Buffer]({{< ref "lec-06.md" >}})
- [Lecture 07: Synchronization 3 - Lock Implementation, Atomic Instructions, Monitors]({{< ref "lec-07.md" >}})
- [Lecture 08: Synchronization 4 - Readers/Writers and Language-Level Support]({{< ref "lec-08.md" >}})

### 调度

- [Lecture 09: Scheduling 1 - Concepts and Classic Policies]({{< ref "lec-09.md" >}})
- [Lecture 10: Scheduling 2 - Fairness, Real Time, and Linux Schedulers]({{< ref "lec-10.md" >}})
- [Lecture 11: Scheduling & Deadlock]({{< ref "lec-11.md" >}})
- [Lecture 12: Scheduling in Modern Computer Systems]({{< ref "lec-12.md" >}})

### 虚拟内存

- [Lecture 13: Address Translation and Virtual Memory]({{< ref "lec-13.md" >}})
- [Lecture 14: Multi-Level Page Tables, TLBs, and Caches]({{< ref "lec-14.md" >}})
- [Lecture 15: TLB/Cache Interaction and Demand Paging]({{< ref "lec-15.md" >}})
- [Lecture 16: Memory 4 - Page Replacement, Clock, and Thrashing]({{< ref "lec-16.md" >}})
- [Lecture 17: Memory 5 - Memory Management in Modern Computer Systems]({{< ref "lec-17.md" >}})

### I/O 与文件系统

- [Lecture 18: I/O - General I/O, Disk, and SSD]({{< ref "lec-18.md" >}})
- [Lecture 19: File System 1 - I/O Performance and File System Design]({{< ref "lec-19.md" >}})
- [Lecture 20: File System Case Studies and Buffering]({{< ref "lec-20.md" >}})
- [Lecture 21: Buffering, Reliability, and Transactions]({{< ref "lec-21.md" >}})
- [Lecture 22: Transactions and Distributed Decision Making]({{< ref "lec-22.md" >}})
- [Lecture 23: Storage and File Systems in Modern Computer Systems]({{< ref "lec-23.md" >}})

## 阅读方式

如果只是快速回顾，可以先看每一讲的导读和本讲地图；如果要补细节，再顺着正文里的图和表往下读。操作系统这门课的重点不在于记住某个孤立机制，而在于把“抽象是什么、状态在哪里、谁能修改、出错后怎么办”这几个问题反复问清楚。
