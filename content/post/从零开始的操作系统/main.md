---
title: 从零开始的操作系统
date: 2026-06-22
categories: 
    - 操作系统
    - 算法
seriesExclude: true
---

## 前言

这是北京大学《操作系统（实验班）》的课程笔记，本课程由金鑫老师教授。

## 阅读入口

### 系统抽象

- [Lecture 01: What is an Operating System? / Four Fundamental OS Concepts]({{< ref "lec-01.md" >}})
- [Lecture 02: Abstractions 1: Threads and Processes]({{< ref "lec-02.md" >}})
- [Lecture 03: Abstractions 2: Files and I/O]({{< ref "lec-03.md" >}})
- [Lecture 04: Abstractions 3: IPC, Pipes and Sockets]({{< ref "lec-04.md" >}})

### 并发同步

- [Lecture 05: Synchronization 1: Concurrency]({{< ref "lec-05.md" >}})
- [Lecture 06: Synchronization 2: Semaphores and Bounded Buffer]({{< ref "lec-06.md" >}})
- [Lecture 07: Synchronization 3: Lock Implementation, Atomic Instructions, and Monitors]({{< ref "lec-07.md" >}})
- [Lecture 08: Synchronization 4: Readers/Writers]({{< ref "lec-08.md" >}})

### 调度

- [Lecture 09: Scheduling 1: Concepts and Classic Policies]({{< ref "lec-09.md" >}})
- [Lecture 10: Scheduling 2: Case Studies, Fairness, Real Time, and Forward Progress]({{< ref "lec-10.md" >}})
- [Lecture 11: Scheduling 3: Scheduling & Deadlock]({{< ref "lec-11.md" >}})
- [Lecture 12: Scheduling 4: Scheduling in Modern Computer Systems]({{< ref "lec-12.md" >}})

### 虚拟内存

- [Lecture 13: Memory 1: Address Translation and Virtual Memory]({{< ref "lec-13.md" >}})
- [Lecture 14: Memory 2: Virtual Memory, Caching and TLBs]({{< ref "lec-14.md" >}})
- [Lecture 15: Memory 3: Demand Paging]({{< ref "lec-15.md" >}})
- [Lecture 16: Memory 4: Page Replacement, Clock, and Thrashing]({{< ref "lec-16.md" >}})
- [Lecture 17: Memory 5: Memory Management in Modern Computer Systems]({{< ref "lec-17.md" >}})

### I/O 与文件系统

- [Lecture 18: I/O: General I/O, Disk and SSD]({{< ref "lec-18.md" >}})
- [Lecture 19: File System 1: I/O Performance and File System Design]({{< ref "lec-19.md" >}})
- [Lecture 20: File System 2: File System Case Studies and Buffering]({{< ref "lec-20.md" >}})
- [Lecture 21: File System 3: Buffering, Reliability, and Transactions]({{< ref "lec-21.md" >}})
- [Lecture 22: File System 4: Transactions and Distributed Decision Making]({{< ref "lec-22.md" >}})
- [Lecture 23: File System 5: Storage and File Systems in Modern Computer Systems]({{< ref "lec-23.md" >}})

## 阅读方式

如果只是快速回顾，可以先看每一讲的导读和本讲地图；如果要补细节，再顺着正文里的图和表往下读。操作系统这门课的重点不在于记住某个孤立机制，而在于把“抽象是什么、状态在哪里、谁能修改、出错后怎么办”这几个问题反复问清楚。
