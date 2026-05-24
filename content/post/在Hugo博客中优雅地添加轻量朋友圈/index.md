---
title: 在Hugo博客中优雅地添加轻量朋友圈
date: 2026-05-24
categories:
    - 建站
image: 10.jpg
updates:
    - date: 2026-05-24
      content: 补充 Friend Circle 效果图，并整理 Stack 主题友链页接入说明。
---

## 前言

友链页通常是一个很安静的页面：头像、站名、一句话简介，然后就结束了。

但是博客本身不是静态的。朋友们会写新文章，会换主题，会突然开始折腾一个很奇妙的项目。只把友链做成一组卡片，某种意义上有点浪费，因为读者很难知道这些站点最近发生了什么。

所以笔者给博客加了一个小功能：在友链页面的朋友卡片下方，额外显示一个 `Friend Circle`，用来展示朋友们最近更新的文章。效果可以直接看本站的示例页面：

<https://www.elainafan.one/friends/>

这个项目现在单独放在 GitHub 上：

<https://github.com/elainafan/hugo-friend-circle>

它的核心目标很简单：**不需要后端，不需要数据库，只靠 RSS / Atom、少量 HTML 兜底解析和 GitHub Actions，让 Hugo 静态博客也能拥有一个友链朋友圈。**

下面先预留两张效果图位置，后面可以把截图放在本文目录下，文件名保持一致即可。

![友链页整体效果，普通友链卡片下方接入 Friend Circle](1.png)

## 基本思路

整个流程可以拆成四步：

1. 在 `data/friends.yaml` 里维护朋友站点信息。
2. 用 `scripts/fetch_feeds.py` 抓取朋友的 RSS / Atom，或者在没有 RSS 时尝试从归档页解析文章链接。
3. 生成 Hugo 可以读取的 `data/friend_posts.json`。
4. Hugo 页面读取这个 JSON，把文章列表渲染到友链页里。

也就是说，页面本身仍然是纯静态的。真正的“更新”发生在构建前，或者发生在 GitHub Actions 定时运行脚本并提交数据的时候。

这个结构的好处是很明显的：部署时不需要额外服务器，也不需要维护一个数据库。对于大多数个人博客来说，这种复杂度刚刚好。

## 配置朋友列表

首先从项目里复制这些文件到自己的 Hugo 站点根目录：

- `scripts/fetch_feeds.py`
- `data/friends.yaml`
- `data/friend_posts.json`
- `layouts/page/friends-circle.html`
- `.github/workflows/update.yml`

其中最重要的是 `data/friends.yaml`。一个最小配置大概长这样：

```yaml
settings:
  max_posts: 240
  max_posts_per_friend: 24
  max_days: 180
  since: 2024-01-01
  timeout: 8
  retries: 2

friends:
  - name: Example Friend
    site: https://example.com/
    feed: https://example.com/index.xml
    avatar: https://example.com/avatar.png
    description: A friend with RSS.

  - name: HTML Only Friend
    site: https://example.org/
    avatar: https://example.org/avatar.png
    description: No RSS exposed; fallback will try dated links on homepage and archives.
```

这里的 `feed` 不是必填项。如果没有填写，脚本会先尝试在站点首页寻找 RSS / Atom 的 `<link rel="alternate">`，如果还是找不到，就会继续尝试解析首页、`/archives/`、`/posts/` 和 `/post/` 里的文章链接。

需要注意的是，HTML 兜底解析不可能覆盖所有博客主题。它更适合那种归档页里有明确日期和文章标题的站点。如果朋友的博客结构非常特殊，最稳妥的办法仍然是让对方暴露一个 RSS 或 Atom feed。

## 处理慢站点和失效站点

友链里经常会遇到两类情况。

第一类是站点还活着，但是网络很慢。这种可以给单个朋友单独调大 `timeout` 和 `retries`：

```yaml
  - name: Slow Friend
    site: https://slow.example/
    feed: https://slow.example/rss.xml
    avatar: https://slow.example/avatar.png
    timeout: 25
    retries: 3
```

第二类是域名过期、站点关掉，或者暂时没有可解析的 RSS。这种情况下，不一定要把友链删掉，可以只让它不参与朋友圈抓取：

```yaml
  - name: Offline Friend
    site: https://old-domain.example/
    avatar: https://old-domain.example/avatar.png
    description: Keep the link card, but skip friend-circle crawling.
    circle: false
    circle_reason: domain unavailable
```

这样它仍然可以留在友链卡片里，但不会拖慢或污染 `Friend Circle` 的数据。

## 本地生成数据

配置好 `data/friends.yaml` 后，在 Hugo 站点根目录运行：

```powershell
python scripts\fetch_feeds.py
```

脚本会生成或更新 `data/friend_posts.json`。这个文件里包含朋友名称、头像、文章标题、文章链接、发布时间、来源站点，以及抓取失败时的 warning。

如果只想从 2024 年之后开始抓，可以在配置里写：

```yaml
settings:
  since: 2024-01-01
```

这比单纯用 `max_days` 更直观。比如现在是 2026 年，那么 `since: 2024-01-01` 就能覆盖 2024 到 2026 年的文章。对于刚开始搭建朋友圈的站点来说，适当多抓一点历史文章会让页面不至于显得太空。

## 创建独立页面

最直接的用法是创建一个独立页面，例如 `content/friends-circle/index.md`：

```yaml
---
title: "Friend Circle"
description: "Recent posts from friends."
layout: "friends-circle"
slug: "friends-circle"
comments: false
---
```

然后 `layouts/page/friends-circle.html` 会读取 `site.Data.friend_posts`，渲染出文章列表。

这个方式适合想把朋友圈单独放进菜单的人。配置简单，迁移也方便。

## 接入 Stack 主题友链页

本站没有把朋友圈做成一个单独页面，而是放在原来的友链页面下方。这样读者先看到普通友链卡片，再继续往下看朋友们最近写了什么，逻辑上会自然一些。

Stack 主题里，友链卡片通常由 `layouts/partials/article/components/links.html` 负责渲染。笔者在这个 partial 的末尾加了一段：

```html
{{ if or .Params.friendCircle (eq .Params.slug "friends") }}
    {{ partial "article/components/friend-circle" . }}
{{ end }}
```

然后把朋友圈主体放在 `layouts/partials/article/components/friend-circle.html`。这个 partial 读取 `data/friend_posts.json`：

```html
{{ $data := site.Data.friend_posts | default dict }}
{{ $posts := $data.posts | default slice }}
{{ $friends := $data.friends | default slice }}
{{ $warnings := $data.warnings | default slice }}
```

页面上的每个文章卡片只保留头像、文章标题和日期，不显示摘要。这样信息密度更高，也不至于让友链页变得太长。

![Friend Circle 卡片样式，显示头像、文章标题和日期](3.png)

此外，前端还加了三个小交互：

- 搜索文章或朋友。
- 按朋友筛选。
- 默认只展示前几条，点击 `Load More` 后继续展开。

这里没有引入额外前端库，只用一点原生 JavaScript 就够了。因为数据在 Hugo 构建时已经写进页面，筛选和展开只是在已有 DOM 上切换显示状态。

## 定时更新

如果博客托管在 GitHub 上，最省事的做法是用 GitHub Actions 定时运行脚本，然后把生成的 `data/friend_posts.json` 提交回仓库。

可以在自己的博客仓库里写一个 workflow：

```yaml
name: update friend circle

on:
  schedule:
    - cron: "0 */3 * * *"
  workflow_dispatch:
  push:
    paths:
      - "data/friends.yaml"
      - "scripts/fetch_feeds.py"

permissions:
  contents: write

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.x"
      - name: Fetch feeds
        run: python scripts/fetch_feeds.py
      - name: Commit generated data
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: update friend circle data"
          file_pattern: data/friend_posts.json
```

如果像本站一样使用 Vercel 部署，那么这种“定时提交生成数据”的方式也很合适：GitHub Actions 更新 JSON 后产生一次提交，Vercel 看到仓库更新，就会重新部署站点。

当然，这种方式会产生自动提交。如果不喜欢仓库历史里有很多 `chore: update friend circle data`，也可以改成在部署流程里先运行脚本，再执行 `hugo --minify`。不过这样需要让部署平台支持定时构建，否则页面不会自动刷新。

## 一些实际踩坑

首先，不要把自己的个人友链数据提交到模板仓库里。开源项目里只应该放示例 `friends.yaml` 和空的 `friend_posts.json`，真正的朋友列表放在自己的博客仓库就好。

其次，抓不到文章不一定是脚本坏了。有些站点没有 RSS，有些站点的 RSS 地址不是常见路径，还有些站点虽然首页能打开，但归档页结构不适合通用 HTML 解析。脚本能做的是尽量泛化，而不是针对某个朋友写死特殊规则。

再次，失效站点最好显式标记 `circle: false`。友链可以保留，但朋友圈抓取应该尽量只处理还能正常访问的站点。

最后，朋友圈的展示不要贪多。摘要、作者、标签、封面都可以加，但对于友链页来说，头像、标题和日期已经足够表达“朋友最近写了什么”。信息越轻，页面越像一个入口，而不是另一个复杂的信息流。

## 结语

这个小项目的定位并不是替代 RSS 阅读器，而是让原本静态的友链页稍微活起来一点。

对于 Hugo 博客来说，RSS、数据文件和 GitHub Actions 本来就是很自然的一组工具。把它们串起来之后，就能在不引入后端的情况下得到一个还算实用的 `Friend Circle`。

如果你也在用 Hugo，可以直接从这个仓库开始：

<https://github.com/elainafan/hugo-friend-circle>
