---
title: 从零开始的博客
date: 2026-05-20
categories:
    - 建站
updates:
    - date: 2026-07-16
      content: 将四篇建站记录整理为主页与子页，保留原文细节，并同步已经变化的代码和文件路径。
seriesExclude: true
---

这个站点使用 Hugo `v0.131.0` 和 Stack `v3.26.0`，由 Vercel 部署。主题外观、文章交互和独立功能页都通过站点目录中的覆盖文件实现，没有直接修改 `themes/hugo-theme-stack`。

## 建站记录

- [自定义美化 Stack 主题]({{< ref "stack-theme.md" >}})：卡片与页面布局、背景图、PhotoSwipe、代码块、阅读进度、系列导航、文章加密、页脚统计和图库。
- [在博客中优雅地引入音乐播放器]({{< ref "music-player.md" >}})：原生 `Audio` 播放器、Bilibili 收藏夹同步、分 P 拆分、播放状态、PJAX 和组件重新初始化。
- [在博客中优雅地添加 Bangumi 追番页面]({{< ref "bangumi.md" >}})：收藏缓存、状态面板、评分与年份视图、详情弹层和公共动画随机推荐。
- [在 Hugo 博客中优雅地添加轻量朋友圈]({{< ref "friend-circle.md" >}})：RSS / Atom 抓取、HTML 兜底、失效站点处理、GitHub Actions 和友链页内嵌。

## 站点结构

```text
assets/
├── scss/custom.scss          自定义样式入口
├── scss/custom/              页面、代码块和功能组件样式
├── scss/music-player.scss    悬浮播放器样式
├── js/music-player.js        播放器状态与播放逻辑
└── ts/main.ts                主题交互、灯箱、进度条和功能页脚本

layouts/
├── partials/                 Stack 模板覆盖与页面组件
├── page/                     Anime、Timeline 等自定义页面
├── shortcodes/bangumi.html   Bangumi 收藏墙
└── _default/_markup/         Markdown 图片和链接渲染

scripts/                      音乐、Bangumi、Friend Circle 数据同步
data/                         构建时读取的歌单、收藏与友链文章数据
```

普通外观从 `assets/scss/custom.scss` 进入，具体样式分散到 `assets/scss/custom/` 下。页面结构由 `layouts` 中的同名模板覆盖主题。需要联网获取的数据先由脚本落到 `data`，Hugo 构建时读取本地结果；外部 API 暂时不可用时，已经同步的数据仍然可以继续生成页面。

## 本地更新

播放器歌单、Bangumi 收藏和 Friend Circle 分别使用自己的同步脚本：

```powershell
python scripts\sync_music.py bilibili
python scripts\sync_bangumi.py
python scripts\fetch_friend_feeds.py
```

其中 `sync_music.py` 会同时整理 `static/music` 与 `data/music/generated.json`，`sync_bangumi.py` 更新 `data/bangumi/anime.json`，`fetch_friend_feeds.py` 更新 `data/friend_posts.json`。这些生成结果保存在博客仓库中，Vercel 不需要在每次部署时重新抓取全部外部数据。

提交前使用仓库内的 Hugo Extended 检查构建：

```powershell
.\hugo.exe --minify
```

Vercel 仍然负责线上部署；GitHub Actions 只用于需要定时刷新的数据，不接管博客构建。

## 旧链接

四个子页保留了原来的 slug，并用 `aliases` 接住旧文章地址。它们设置为 `hidden: true`，首页与分类页只显示这篇主页；进入任意子页后，可以通过文章底部的系列导航前后切换或返回主页。
