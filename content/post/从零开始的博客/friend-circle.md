---
title: Friend Circle
date: 2026-05-24
slug: friend-circle
aliases:
    - /p/在hugo博客中优雅地添加轻量朋友圈/
hidden: true
seriesOrder: 4
---

普通友链页只说明“这些站点值得去看”，却看不出朋友最近写了什么。本站在原有友链卡片下接了一段 `Friend Circle`，聚合朋友博客的 RSS、Atom 或公开文章列表。

示例页面是 [Elainafan 的友链页](https://www.elainafan.one/friends/)，可复用的独立项目放在 [elainafan/hugo-friend-circle](https://github.com/elainafan/hugo-friend-circle)。博客仓库保留自己的朋友数据，开源项目只提供通用脚本、模板和接入方式。

![友链页中的 Friend Circle](friend-circle-1.png)

## 数据配置

朋友信息写在 `data/friends.yaml`。全局设置控制总文章数、每位朋友的上限、时间范围、超时和重试次数：

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
```

`feed` 可以省略。脚本会从首页的 `<link rel="alternate">` 发现 RSS 或 Atom，也会尝试常见的 `/index.xml`、`/rss.xml`、`/feed.xml` 等地址。

慢站点可以单独放宽超时，不必拖慢所有朋友：

```yaml
  - name: Slow Friend
    site: https://slow.example.com/
    feed: https://slow.example.com/rss.xml
    timeout: 25
    retries: 3
```

已经失效、没有订阅源或不希望进入朋友圈的站点继续保留在普通友链中，并在抓取配置里关闭：

```yaml
    circle: false
    circle_reason: 域名暂时不可达
```

这样不会每次更新都等待一个确定失败的请求，友链关系也不会因为暂时停站而被删除。

## 抓取文章

脚本是 `scripts/fetch_friend_feeds.py`，输出到 `data/friend_posts.json`：

```powershell
python scripts\fetch_friend_feeds.py
```

RSS 与 Atom 会先按 XML 命名空间解析。拿不到 feed 时，脚本再访问站点首页以及 `/archives/`、`/posts/`、`/post/`，从带日期的公开链接中提取文章。HTML 兜底面向常见博客结构，不可能识别所有主题；站点有稳定 feed 时，显式填写仍然最可靠。

抓取结果会经过几层清理：

- 过滤早于 `since` 或超出 `max_days` 的文章。
- 丢弃明显晚于当前时间的异常日期。
- 统一相对链接，按最终 URL 去重。
- 清理标题中的 HTML 标签与转义实体。
- 每位朋友只保留 `max_posts_per_friend` 条，再按时间合并。

某个站点超时或解析失败时，只向 `warnings` 写入记录。脚本仍会生成其余朋友的数据并返回成功，单个失效 feed 不会让整次构建报废。

生成文件包含抓取时间、朋友状态、警告和文章列表。Hugo 构建阶段只读这份 JSON，不会在模板中联网。

## 接进友链页

普通友链仍由 `content/page/link/index.md` 的 `links` frontmatter 管理。`layouts/partials/article/components/links.html` 渲染完朋友卡片后，根据页面 slug 插入朋友圈：

```go-html-template
{{ if or .Params.friendCircle (eq .Params.slug "friends") }}
    {{ partial "article/components/friend-circle" . }}
{{ end }}
```

因此 Friend Circle 不是新的独立页面，也不会增加左侧菜单项。它只出现在 `/friends/` 的普通朋友卡片下方。

`layouts/partials/article/components/friend-circle.html` 读取 `site.Data.friend_posts`，顶部显示朋友数、文章数和生成时间。工具栏提供关键词搜索和朋友筛选；筛选值直接使用卡片上的 `data-friend`，不会再出现下拉框变化后列表没有反应的问题。

文章卡片只显示头像、标题和日期，不渲染摘要：

```go-html-template
<article data-fc-item data-friend="{{ .friend }}">
  <a href="{{ .site }}" target="_blank" rel="noopener">
    <img src="{{ .avatar }}" alt="{{ .friend }}" loading="lazy">
  </a>
  <div>
    <a href="{{ .url }}" target="_blank" rel="noopener">{{ $title }}</a>
    <time datetime="{{ $published }}">{{ $published }}</time>
  </div>
</article>
```

标题在模板中再次执行 `htmlUnescape`、去标签与空白归一化，RSS 里残留的 `<span style=...>` 不会直接出现在卡片上。

![头像、文章标题与日期](friend-circle-2.png)

页面初始显示 8 条。点击 `Load More` 后再增加 8 条；搜索或切换朋友时，显示上限会回到第一页。按钮只在仍有隐藏结果时出现，旁边同步显示“已显示 n / m”。

抓取警告收进 `<details>`，默认不占版面。需要检查哪位朋友的 feed 失效时再展开。

## 定时更新

GitHub Actions 配置位于 `.github/workflows/update-friends.yml`，每三小时运行一次，也支持手动触发：

```yaml
on:
  schedule:
    - cron: "0 */3 * * *"
  workflow_dispatch:
  push:
    paths:
      - "data/friends.yaml"
      - "scripts/fetch_friend_feeds.py"
```

工作流只提交生成数据：

```yaml
- name: Fetch feeds
  run: python scripts/fetch_friend_feeds.py

- name: Commit generated data
  uses: stefanzweifel/git-auto-commit-action@v5
  with:
    commit_message: "chore: update friend circle data"
    file_pattern: data/friend_posts.json
```

Vercel 发现仓库新提交后重新部署，友链页随之更新。定时提交保留了每次抓取结果，也避免在每次普通博客构建中重复访问所有朋友站点。
