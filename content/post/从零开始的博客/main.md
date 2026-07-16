---
title: 从零开始的博客
date: 2026-05-20
categories:
    - 建站
updates:
    - date: 2026-07-16
      content: 按当前站点实现整理主题、播放器、Bangumi 与 Friend Circle 的文档入口。
seriesExclude: true
---

本站使用 Hugo `v0.131.0` 与 Stack `v3.26.0`，部署在 Vercel。主题目录保持原样，站点自己的模板、样式和脚本分别放在 `layouts`、`assets` 与 `scripts` 中。升级 Stack 时，只需检查这些覆盖文件与新版本模板是否仍然兼容。

## 主题与文章

### [Stack 主题]({{< ref "stack-theme.md" >}})

卡片布局、背景、PhotoSwipe、代码块、阅读进度、系列导航、文章加密、页脚统计与图库都由站点覆盖文件实现。样式按用途拆进 `assets/scss/custom/`，模板集中在 `layouts`。

### [音乐播放器]({{< ref "music-player.md" >}})

原生 `Audio` 负责播放，歌单由 Bilibili 收藏夹与本地音乐目录共同生成。站点脚本维护播放模式、进度恢复、文章曲目联动与 PJAX 初始化，切换文章时不会重新创建播放器。

## 独立页面

### [Bangumi]({{< ref "bangumi.md" >}})

番剧页读取本地 Bangumi 收藏缓存，按状态展示条目，并提供个人评分、年份视图、详情弹层与公共动画随机推荐。

### [Friend Circle]({{< ref "friend-circle.md" >}})

友链页下方聚合朋友们的 RSS / Atom，缺少 feed 时再尝试 HTML 解析。抓取结果写入 Hugo data，卡片只显示头像、文章标题和日期；失效站点不会拖住整轮更新。

## 文件位置

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

`assets/scss/custom.scss` 是普通样式入口，具体规则分散在 `assets/scss/custom/`。`layouts` 中的同名模板覆盖 Stack，联网数据则由脚本写入 `data`。Hugo 构建只读取已经落盘的结果，外部 API 暂时不可用时仍能生成页面。

## 本地更新

播放器歌单、Bangumi 收藏和 Friend Circle 分别使用自己的同步脚本：

```powershell
python scripts\sync_music.py bilibili
python scripts\sync_bangumi.py
python scripts\fetch_friend_feeds.py
```

`sync_music.py` 同时整理 `static/music` 与 `data/music/generated.json`，`sync_bangumi.py` 更新 `data/bangumi/anime.json`，`fetch_friend_feeds.py` 更新 `data/friend_posts.json`。生成结果保存在博客仓库中，Vercel 部署时不必重新抓取全部外部数据。

提交前使用仓库内的 Hugo Extended 检查构建：

```powershell
.\hugo.exe --minify
```

Vercel 负责线上部署，GitHub Actions 只刷新需要定时更新的数据，不接管博客构建。
