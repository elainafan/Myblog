---
title: 从零开始的博客
date: 2026-05-20
categories:
    - 建站
updates:
    - date: 2026-07-16
      content: 将建站文章整理为主页与四个子页，并按当前代码重写播放器、Bangumi 和 Friend Circle 说明。
seriesExclude: true
---

这个站点以 Hugo `v0.131.0` 和 Stack `v3.26.0` 为底座，部署交给 Vercel。主题外观、文章交互和几个独立功能页都由站点目录中的覆盖文件完成，没有直接修改 `themes/hugo-theme-stack`。

## 目录

- [Stack 主题改造]({{< ref "stack-theme.md" >}})
- [音乐播放器与 PJAX]({{< ref "music-player.md" >}})
- [Bangumi 收藏墙]({{< ref "bangumi.md" >}})
- [Friend Circle]({{< ref "friend-circle.md" >}})

## 站点结构

自定义代码主要分在四个目录中。

```text
assets/     SCSS、TypeScript、播放器脚本和图片资源
layouts/    对 Stack 模板的覆盖、自定义页面和 shortcode
scripts/    歌单、Bangumi、Friend Circle 等数据同步脚本
data/       构建时读取的歌单、收藏与友链文章数据
```

普通外观从 `assets/scss/custom.scss` 进入；页面结构由 `layouts` 中的同名模板覆盖主题；需要联网获取的数据先由脚本落到 `data`，Hugo 构建时只读取本地结果。这样即使外部 API 暂时不可用，已生成的页面也不会跟着消失。

四个子页都保留了原文章地址。旧链接会跳到新的系列子页，分类页与首页只显示这篇主页，不会被隐藏的教程页刷满。
