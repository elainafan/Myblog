---
title: 在博客中优雅地添加Bangumi追番页面
date: 2026-03-13
slug: bangumi-wall
aliases:
    - /p/在博客中优雅地添加bangumi追番页面/
hidden: true
seriesOrder: 3
updates:
    - date: 2026-07-16
      content: 按当前 Bangumi 收藏墙实现整理数据同步、筛选与交互说明。
---

## 数据

### 收藏接口

Bangumi 用户收藏需要公开可访问。动画收藏接口为：

```text
https://api.bgm.tv/v0/users/<user-id>/collections?subject_type=2&limit=100&offset=0
```

`subject_type=2` 表示动画，`limit` 与 `offset` 用于分页。页面使用以下字段：

| 字段 | 含义 |
| --- | --- |
| `type` | 收藏状态，比如想看、看过、在看、搁置 |
| `rate` | 用户评分 |
| `comment` | 用户短评 |
| `ep_status` | 当前看到第几集 |
| `subject.name_cn` | 中文标题 |
| `subject.images.common` | 封面图 |
| `subject.score` | Bangumi 站内均分 |
| `subject.rank` | Bangumi 排名 |

Bangumi 收藏变化后重新运行同步脚本，页面便会使用新数据。

### 本地缓存

`scripts/sync_bangumi.py` 把公开收藏整理为 Hugo data 文件，避免 Bangumi API 临时不可用时出现空页面。

脚本分页请求收藏接口，只保留页面使用的字段：

```python
DEFAULT_USER = "your-user-id"
DEFAULT_OUTPUT = Path("data/bangumi/anime.json")
API_ROOT = "https://api.bgm.tv/v0"
```

每个条目整理为下面的结构：

```json
{
  "subject_id": 123456,
  "type": 3,
  "rate": 0,
  "ep_status": 0,
  "comment": "",
  "subject": {
    "name": "Example Title",
    "name_cn": "示例标题",
    "date": "2026-01-01",
    "score": 8.0,
    "rank": 100,
    "eps": 12,
    "images": {
      "common": "https://example.com/cover.jpg"
    }
  }
}
```

在博客根目录运行：

```bash
python scripts/sync_bangumi.py
```

脚本生成 `data/bangumi/anime.json`。文件只保存公开收藏和作品元数据，不含登录态，也不需要在仓库中存放 token 或 cookie。

## 页面

### Shortcode

`layouts/shortcodes/bangumi.html` 默认读取 `data/bangumi/anime.json`。只有显式打开 `live` 时，构建过程才会请求 Bangumi API：

```go-html-template
{{- $user := .Get "user" | default (.Page.Params.bangumi.user | default (.Site.Params.bangumi.user | default "your-user-id")) -}}
{{- $limit := .Get "limit" | default (.Page.Params.bangumi.limit | default (.Site.Params.bangumi.limit | default 100)) -}}
{{- $live := .Get "live" | default (.Page.Params.bangumi.live | default (.Site.Params.bangumi.live | default false)) -}}
{{- $bangumiData := .Site.Data.bangumi.anime | default dict -}}
{{- $source := "cache" -}}
{{- if $live -}}
    {{- $apiURL := printf "https://api.bgm.tv/v0/users/%s/collections?subject_type=2&limit=%v&offset=0" $user $limit -}}
    {{- $opts := dict "headers" (dict "Accept" "application/json" "User-Agent" "HugoBlog/1.0 (https://example.com)") -}}
    {{- $res := resources.GetRemote $apiURL $opts -}}
    {{- if and $res (not $res.Err) -}}
        {{- $bangumiData = $res.Content | transform.Unmarshal -}}
        {{- $source = "live" -}}
    {{- else -}}
        {{- warnf "获取 Bangumi 收藏数据失败，使用本地缓存。" -}}
    {{- end -}}
{{- end -}}
```

`{{</* bangumi live=true */>}}` 打开构建期实时请求；未设置时读取本地缓存。

### 页面头部

页面头部显示标题、说明、收藏总数、最近更新时间，以及 Bangumi 主页链接：

```go-html-template
<header class="bangumi-hero">
    <div>
        <div class="bangumi-title" role="heading" aria-level="2">Bangumi 动画收藏</div>
        <p class="bangumi-desc">记录最近在看、看过和想看的动画。</p>
        <div class="bangumi-stats">
            共 {{ len $items }} 条收藏
            {{ with $bangumiData.fetched_at }}
                · 最近更新：{{ time.Format "2006-01-02" . }}
            {{ end }}
        </div>
    </div>
    <a class="bangumi-home" href="https://bangumi.tv/user/{{ $user }}" target="_blank" rel="noopener noreferrer">查看 Bangumi 主页 ↝</a>
</header>
```

![Bangumi 动画收藏页面](bangumi-1.png)

### 状态分组

收藏按 Bangumi 状态分组：

```go-html-template
{{- $groups := slice
    (dict "type" 3 "label" "在看" "name" "watching")
    (dict "type" 2 "label" "看过" "name" "watched")
    (dict "type" 1 "label" "想看" "name" "wish")
    (dict "type" 4 "label" "搁置" "name" "on-hold")
    (dict "type" 5 "label" "抛弃" "name" "dropped")
-}}
```

状态导航遍历有内容的分组，点击按钮时显示对应面板：

```go-html-template
<nav class="bangumi-tabs" aria-label="Bangumi 收藏状态">
    {{ range $groups }}
        {{ $groupItems := where $items "type" .type }}
        {{ if gt (len $groupItems) 0 }}
            <button class="bangumi-tab" type="button" data-bangumi-tab="{{ .name }}">
                {{ .label }}
            </button>
        {{ end }}
    {{ end }}
</nav>
```

较长的分组按批次显示，`Load More` 继续展开当前分组；“看过”分组还可以在评分顺序与年份视图之间切换。

“随机一部”从 Bangumi 公共动画条目中取得候选，不局限于用户收藏。远程请求失败或超时时改用本地候选池，结果仍保留封面、评分和 Bangumi 条目链接。

### 卡片与详情

卡片默认显示封面、标题、年份和评分。个人短评、观看进度与 Bangumi 排名收在封面悬停层中：

```go-html-template
{{ range $groupItems }}
    {{ $subject := .subject }}
    {{ $title := $subject.name_cn | default $subject.name | default "Untitled" }}
    {{ $cover := $subject.images.common | default $subject.images.medium | default $subject.images.large }}
    {{ $eps := $subject.eps | default 0 }}
    {{ $epStatus := .ep_status | default 0 }}
    {{ $siteScore := $subject.score | default 0 }}
    {{ $rank := $subject.rank | default 0 }}
    {{ $hasProgress := and (gt $eps 0) (gt $epStatus 0) }}
    <a class="bangumi-card" href="https://bangumi.tv/subject/{{ .subject_id }}" target="_blank" rel="noopener noreferrer">
        <div class="bangumi-cover">
            <img src="{{ $cover }}" alt="{{ $title }}" loading="lazy" referrerpolicy="no-referrer">
            {{ if gt .rate 0 }}
                <span class="bangumi-score">{{ .rate }}</span>
            {{ end }}
            <div class="bangumi-extra">
                {{ if gt $rank 0 }}
                    <span class="bangumi-extra-line">Bangumi #{{ $rank }}</span>
                {{ end }}
                {{ if $hasProgress }}
                    <span class="bangumi-extra-line">进度 {{ $epStatus }} / {{ $eps }}</span>
                {{ end }}
                {{ with .comment }}
                    <span class="bangumi-extra-comment">{{ . }}</span>
                {{ end }}
            </div>
        </div>
        <div class="bangumi-info">
            <div class="bangumi-name" role="heading" aria-level="4">{{ $title }}</div>
            <div class="bangumi-meta">
                {{ with $subject.date }}<span>{{ substr . 0 4 }}</span>{{ end }}
                {{ if gt $siteScore 0 }}<span>Bangumi {{ $siteScore }}</span>{{ end }}
            </div>
        </div>
    </a>
{{ end }}
```

普通点击先打开轻量详情弹层，展示封面、标题、个人评分、Bangumi 分数、排名、进度和短评。弹层内提供 Bangumi 条目链接，`Ctrl` / `Command` 点击卡片则直接在新标签页打开。

![Bangumi 收藏详情弹层](bangumi-2.png)

样式沿用 Stack 的 `var(--card-background)`、`var(--shadow-l2)` 和文字颜色变量，亮色与暗色模式共用同一套结构。

## 页面入口

页面位于 `content/page/anime/index.md`，正文只有 frontmatter 与 shortcode：

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

`layout: "anime"` 对应 `layouts/page/anime.html`，负责套用 Stack 的文章外壳；番剧数据由 `{{</* bangumi */>}}` 渲染。

## 更新

本站使用本地缓存方式更新：

```bash
python scripts/sync_bangumi.py
```

运行后提交更新的 `data/bangumi/anime.json`。Vercel 构建直接读取该文件，无需等待 Bangumi API。

构建期实时请求使用：

```go-html-template
{{</* bangumi live=true */>}}
```

实时请求失败时，shortcode 会退回本地缓存，因此页面仍能正常生成。
