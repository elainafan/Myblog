---
title: 从零开始的AI编程
date: 2025-09-10
categories:
    - AI
updates:
    - date: 2026-07-22
      content: 补充 Lab 1–7 笔记，按模块实现与调试问题重组内容。
    - date: 2026-07-14
      content: 补齐各讲的实现细节，重组标题层级与阅读顺序。
seriesExclude: true
---

## 前言

这是北京大学《人工智能中的编程》的课程笔记，本课程由王鹏帅、楚梦渝、梁一韬三位老师共同教授。

## 课程笔记

### PyTorch 与 CUDA

- [导论]({{< ref "01-introduction.md" >}})
- [并行编程]({{< ref "02-parallel-programming.md" >}})
- [并行通信]({{< ref "03-parallel-communication.md" >}})
- [并行算法 I]({{< ref "04-parallel-algorithms-1.md" >}})
- [并行算法 II]({{< ref "05-parallel-algorithms-2.md" >}})
- [矩阵乘法]({{< ref "06-matrix-product.md" >}})
- [卷积与池化]({{< ref "07-convolution-pooling.md" >}})
- [PyBind 与单元测试]({{< ref "08-pybind-unit-test.md" >}})

### 框架与编译

- [自动微分]({{< ref "09-auto-diff.md" >}})
- [计算图]({{< ref "10-computational-graph.md" >}})
- [AI 编译器前端]({{< ref "11-compiler-frontend.md" >}})
- [优化]({{< ref "12-optimization.md" >}})
- [AI 编译器后端]({{< ref "13-compiler-backend.md" >}})

### 数据与分布式训练

- [数据处理]({{< ref "14-data-processing.md" >}})
- [异构处理器]({{< ref "15-heterogeneous-processors.md" >}})
- [分布式训练与数据并行]({{< ref "16-distributed-data-parallel.md" >}})
- [模型并行与张量并行]({{< ref "17-model-tensor-parallel.md" >}})

### 部署与联邦学习

- [量化]({{< ref "18-quantization.md" >}})
- [LLM 推理与服务]({{< ref "19-llm-inference-serving.md" >}})
- [联邦学习]({{< ref "20-federated-learning.md" >}})

## Lab 笔记

- [Lab 1：CIFAR-10 图像分类]({{< ref "lab-01.md" >}})
- [Lab 2：Tensor 与激活函数]({{< ref "lab-02.md" >}})
- [Lab 3：CUDA 神经网络算子]({{< ref "lab-03.md" >}})
- [Lab 4：Python 扩展封装]({{< ref "lab-04.md" >}})
- [Lab 5：自动微分]({{< ref "lab-05.md" >}})
- [Lab 6：优化器]({{< ref "lab-06.md" >}})
- [Lab 7：Final Project 与自定义深度学习框架]({{< ref "final-project.md" >}})
