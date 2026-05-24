---
title: 在博客中优雅地添加Bangumi追番页面
date: 2026-03-13
categories:
    - 建站
updates:
    - date: 2026-05-24
      content: 将原 Bilibili 追番方案整体升级为 Bangumi 收藏墙。
image: 1.jpg
---
## 前言
之前笔者在博客里做过一个 Bilibili 追番页面：构建时通过 `resources.GetRemote` 拉取 B 站公开追番 API，然后把结果渲染成一面番剧海报墙。这个方案胜在简单，但继续用下来会发现一个问题：Bilibili 更像播放平台，而不是作品数据库。很多番没有版权、下架、地区不可见，或者剧场版、OVA、续作分得不够稳定，用它来做“番剧收藏页”总觉得差一点。

因此这次把 `/anime/` 页面从 Bilibili 追番墙升级成 Bangumi 收藏墙。Bangumi 的优势在于条目更完整，作品标题、中文名、封面、放送日期、站内评分和排名都能直接拿到；更重要的是，它能保留自己的收藏状态、个人评分、观看进度和短评。这样页面就不只是一个平台列表，而更像一份真正属于自己的番剧记录。

本文仍然以 Hugo 和 Stack 主题为例，整理一个静态博客可用的实现：先用脚本把 Bangumi 公开收藏同步到本地缓存，再通过 shortcode 渲染为分组卡片墙。这样页面加载不依赖前端请求，Vercel 构建时也不会被外部 API 卡住。

> 截图占位：`cover.png` / `1.png`，用于展示 Bangumi 追番页面的整体效果。

## 准备 Bangumi 收藏
首先需要有一个公开可访问的 Bangumi 用户收藏页。比如笔者的用户 ID 是 `1020990`，那么动画收藏可以通过下面这个接口读取：

```text
https://api.bgm.tv/v0/users/1020990/collections?subject_type=2&limit=100&offset=0
```

这里的 `subject_type=2` 表示动画，`limit` 和 `offset` 用来分页。返回结果里比较有用的字段包括：

| 字段 | 含义 |
| --- | --- |
| `type` | 收藏状态，比如想看、看过、在看、搁置 |
| `rate` | 自己给这部番的评分 |
| `comment` | 自己写的短评 |
| `ep_status` | 当前看到第几集 |
| `subject.name_cn` | 中文标题 |
| `subject.images.common` | 封面图 |
| `subject.score` | Bangumi 站内均分 |
| `subject.rank` | Bangumi 排名 |

需要注意的是，Bangumi 账号不用一开始就维护得非常完整。只要有一部分看过、在看或者想看的条目，页面就已经能成型；后面每次在 Bangumi 上更新收藏，博客重新构建时也会跟着刷新。

## 加一个本地缓存脚本
直接在 Hugo 模板里请求远程 API 可以工作，但静态站点构建最怕外部接口偶尔抽风。为了避免某次 Vercel 构建时 Bangumi API 访问失败导致页面空掉，笔者先加了一个同步脚本，把公开收藏整理成 Hugo data 文件。

在 `scripts/sync_bangumi.py` 中写入脚本，核心逻辑是分页请求 Bangumi 收藏接口，然后只保留页面需要的字段：

```python
DEFAULT_USER = "1020990"
DEFAULT_OUTPUT = Path("data/bangumi/anime.json")
API_ROOT = "https://api.bgm.tv/v0"
```

每个条目会被规整成这样的结构：

```json
{
  "subject_id": 262897,
  "type": 3,
  "rate": 9,
  "ep_status": 0,
  "comment": "尸体暖暖的",
  "subject": {
    "name": "ゆるキャン△ SEASON 2",
    "name_cn": "摇曳露营△ 第二季",
    "date": "2021-01-07",
    "score": 8.3,
    "rank": 89,
    "eps": 13,
    "images": {
      "common": "https://lain.bgm.tv/r/400/pic/cover/l/0f/50/262897_d3555.jpg"
    }
  }
}
```

然后在博客根目录运行：

```bash
python scripts/sync_bangumi.py
```

脚本会生成 `data/bangumi/anime.json`。这个文件可以提交到仓库里，作为 API 失败时的兜底缓存。因为里面只保存公开收藏和作品元数据，不涉及 Bangumi 登录态，也不需要把 token 或 cookie 放进仓库。

> 截图占位：`2.png`，用于展示 `data/bangumi/anime.json` 的缓存数据结构。

## 编写 Bangumi Shortcode
接下来改 `layouts/shortcodes/bangumi.html`。这个 shortcode 默认读取 `data/bangumi/anime.json`，也就是上一步同步得到的缓存文件。这样构建过程会更稳，不会因为 Bangumi API 临时变慢而让整站构建超时。

```go-html-template
{{- $user := .Get "user" | default (.Page.Params.bangumi.user | default (.Site.Params.bangumi.user | default "1020990")) -}}
{{- $limit := .Get "limit" | default (.Page.Params.bangumi.limit | default (.Site.Params.bangumi.limit | default 100)) -}}
{{- $live := .Get "live" | default (.Page.Params.bangumi.live | default (.Site.Params.bangumi.live | default false)) -}}
{{- $bangumiData := .Site.Data.bangumi.anime | default dict -}}
{{- $source := "cache" -}}
{{- if $live -}}
    {{- $apiURL := printf "https://api.bgm.tv/v0/users/%s/collections?subject_type=2&limit=%v&offset=0" $user $limit -}}
    {{- $opts := dict "headers" (dict "Accept" "application/json" "User-Agent" "ElainafanBlog/1.0 (https://www.elainafan.one)") -}}
    {{- $res := resources.GetRemote $apiURL $opts -}}
    {{- if and $res (not $res.Err) -}}
        {{- $bangumiData = $res.Content | transform.Unmarshal -}}
        {{- $source = "live" -}}
    {{- else -}}
        {{- warnf "获取 Bangumi 收藏数据失败，使用本地缓存。" -}}
    {{- end -}}
{{- end -}}
```

这里保留了一个可选的 `live` 开关。如果之后想在某个页面里强制构建期实时请求，可以写成 `{{</* bangumi live=true */>}}`；平时则让它读本地缓存，速度和稳定性都会更好。

然后按 Bangumi 收藏状态分组：

```go-html-template
{{- $groups := slice
    (dict "type" 3 "label" "在看" "name" "watching")
    (dict "type" 2 "label" "看过" "name" "watched")
    (dict "type" 1 "label" "想看" "name" "wish")
    (dict "type" 4 "label" "搁置" "name" "on-hold")
    (dict "type" 5 "label" "抛弃" "name" "dropped")
-}}
```

卡片本身只需要从条目里取出封面、标题、年份、评分、进度和短评即可：

```go-html-template
{{ range $groupItems }}
    {{ $subject := .subject }}
    {{ $title := $subject.name_cn | default $subject.name | default "Untitled" }}
    {{ $cover := $subject.images.common | default $subject.images.medium | default $subject.images.large }}
    <a class="bangumi-card" href="https://bangumi.tv/subject/{{ .subject_id }}" target="_blank" rel="noopener noreferrer">
        <div class="bangumi-cover">
            <img src="{{ $cover }}" alt="{{ $title }}" loading="lazy" referrerpolicy="no-referrer">
            {{ if gt .rate 0 }}
                <span class="bangumi-score">{{ .rate }}</span>
            {{ end }}
        </div>
        <div class="bangumi-info">
            <h4 class="bangumi-name">{{ $title }}</h4>
            <div class="bangumi-meta">
                {{ with $subject.date }}{{ substr . 0 4 }}{{ end }}
                {{ with $subject.score }} · Bangumi {{ . }}{{ end }}
                {{ with $subject.rank }} · #{{ . }}{{ end }}
            </div>
            {{ with .comment }}
                <div class="bangumi-comment">{{ . }}</div>
            {{ end }}
        </div>
    </a>
{{ end }}
```

完整样式可以按自己博客的气质调整。笔者这里选择继续沿用 Stack 的 `var(--card-background)`、`var(--shadow-l2)` 和文字颜色变量，这样亮色、暗色模式下都比较自然。

## 创建番剧页面
页面本身仍然放在 `content/page/anime/index.md`。因为主要渲染逻辑已经被 shortcode 接管，这里只需要写 frontmatter 和一行调用：

```yaml
---
title: "番剧 | Anime"
date: 2025-10-26
readingTime: true
layout: "anime"
slug: "anime"
url: "/anime/"
menu:
    main:
        weight: -50
        params:
            icon: eye

comments: true
---

{{</* bangumi */>}}
```

这里的 `layout: "anime"` 对应 `layouts/page/anime.html`。这个 layout 只负责套用 Stack 的文章外壳，真正的番剧数据展示交给 `{{</* bangumi */>}}`。

## 构建和更新方式
之后的更新方式有两种。

主要方式是手动刷新缓存：

```bash
python scripts/sync_bangumi.py
```

然后提交更新后的 `data/bangumi/anime.json`。这样 Vercel 构建时不需要再等 Bangumi API，页面也不会因为外部接口临时抽风而空掉。

如果确实想让 Hugo 在构建时直接抓最新数据，也可以在 shortcode 中显式打开实时模式：

```go-html-template
{{</* bangumi live=true */>}}
```

不过笔者更建议把“同步数据”和“构建博客”分开。前者失败了可以稍后再跑一次，后者则应该尽量稳定。

## 小结
相比 Bilibili 追番墙，Bangumi 版本更适合个人博客。Bilibili 更像“在哪里看”，Bangumi 更像“我看过什么、怎么评价”。当页面显示出自己的评分、进度和短评后，它就不只是装饰性的海报墙，而是一个能长期维护的动画记录页。

后续还可以继续往上加功能，比如按标签筛选、只显示高分推荐、加入观看链接，或者把 Bangumi 的收藏时间做成时间线。不过对一个静态 Hugo 博客来说，现在这个版本已经足够稳定，也足够好看了。
