---
title: 从零开始的AI编程
date: 2025-09-10
categories:
    - AI
updates:
    - date: 2026-07-14
      content: 补回 CUDA、计算图、编译器与优化器中的实现细节和推导。
seriesExclude: true
---

## 前言

这是北京大学《人工智能中的编程》的课程笔记，内容包括 CUDA 与并行算法、自动微分、计算图、AI 编译器、分布式训练和模型部署。

## 阅读入口

### 框架基础

- [导论]({{< ref "01-introduction.md" >}})

### CUDA 与并行计算

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
- [数据处理]({{< ref "14-data-processing.md" >}})
- [异构处理器]({{< ref "15-heterogeneous-processors.md" >}})

### 训练与部署

- [分布式训练与数据并行]({{< ref "16-distributed-data-parallel.md" >}})
- [模型并行与张量并行]({{< ref "17-model-tensor-parallel.md" >}})
- [量化]({{< ref "18-quantization.md" >}})
- [LLM 推理与服务]({{< ref "19-llm-inference-serving.md" >}})
- [联邦学习]({{< ref "20-federated-learning.md" >}})
