---
title: 在博客中优雅地添加Bangumi追番页面
date: 2026-03-13
categories:
    - 建站
updates:
    - date: 2026-05-25
      content: 补充看过列表的年份视图、随机推荐兜底池和番剧详情弹层。
    - date: 2026-05-25
      content: 将看过列表改为按个人评分排序，并加入 Bangumi 公共动画随机推荐。
    - date: 2026-05-25
      content: 精简番剧卡片默认信息，将短评、进度和排名收纳到悬停层。
    - date: 2026-05-25
      content: 增加状态切换导航和分组内 Load More 展开。
    - date: 2026-05-24
      content: 调整 Bangumi 页面头部样式。
    - date: 2026-05-24
      content: 将原 Bilibili 追番方案整体升级为 Bangumi 收藏墙。
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

页面头部则单独做成一块卡片式 hero。这里不再把“缓存数据”做成一排小徽章，而是只保留用户真正关心的信息：标题、说明、收藏总数、最近更新时间，以及跳转到 Bangumi 主页的链接。

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

这个头部看起来会更像一个独立功能页，而不是普通文章里临时塞进去的一段列表。副标题保留“记录最近在看、看过和想看的动画。”，也能让第一次点进来的访客立刻知道这个页面在做什么。

然后按 Bangumi 收藏状态分组：

```go-html-template
{{- $groups := slice
    (dict "type" 3 "label" "在看" "name" "watching" "initial" 0 "step" 8)
    (dict "type" 2 "label" "看过" "name" "watched" "initial" 12 "step" 12)
    (dict "type" 1 "label" "想看" "name" "wish" "initial" 8 "step" 8)
    (dict "type" 4 "label" "搁置" "name" "on-hold" "initial" 8 "step" 8)
    (dict "type" 5 "label" "抛弃" "name" "dropped" "initial" 8 "step" 8)
-}}
```

这里的 `initial` 表示初始显示数量，`step` 表示每次点击 `Load More` 继续展开多少张。`在看` 通常数量很少，所以这里用 `initial: 0` 表示全部显示；`看过` 会比较长，因此默认只显示 12 张。

状态导航不放“全部”，只保留具体状态。点击某个按钮时，页面只显示对应的状态面板：

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

其中 `看过` 这一组可以默认按自己的评分排序。这样页面打开时，最先看到的是笔者真正喜欢的作品，而不是单纯按照同步时间或作品年份排列：

```go-html-template
{{ if eq .name "watched" }}
    {{ $groupItems = sort $groupItems "rate" "desc" }}
{{ end }}
```

不过 `看过` 的条目一多，只按评分看也会丢掉时间感。因此页面里又加了一个小切换：`按评分` 和 `按年份`。评分视图用来看口味，年份视图用来看自己补番的轨迹；切换时不重新请求数据，只是在前端重新排列已有卡片，并在年份视图里插入年份分隔条。

```html
<button class="bangumi-view-button" type="button" data-bangumi-view="rating">按评分</button>
<button class="bangumi-view-button" type="button" data-bangumi-view="year">按年份</button>
```

导航右侧还可以放一个随机推荐按钮。这个按钮不从自己的收藏里抽，而是从 Bangumi 公共动画条目里抽一部站内评分不低于 6 的作品，适合作为“随便看看今天补什么”的入口：

```ts
const offset = Math.floor(Math.random() * 1800);
const response = await fetch(
    `https://api.bgm.tv/v0/subjects?type=2&sort=rank&limit=20&offset=${offset}`
);
```

前端拿到结果后再筛一遍 `rating.score >= 6`，最后把标题、封面、年份、Bangumi 分数和排名渲染到按钮下方的小卡片里。为了避免访问 Bangumi API 失败时按钮完全不可用，这里还准备了一个很小的本地兜底池：请求失败时仍然能给出一部公共高分动画，只是会在结果里标注“本地兜底”。

卡片本身默认只露出封面、标题、年份和评分。个人短评、观看进度和 Bangumi 排名虽然有用，但如果全部铺在卡片上，页面很快就会显得拥挤。因此这里把这些细节收纳到封面悬停层里：平时当作海报墙扫视，鼠标移上去时再看补充信息。

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

卡片点击时也不一定要立刻跳转到 Bangumi。现在的处理是：普通点击先打开一个轻量详情弹层，里面展示封面、标题、个人评分、Bangumi 分数、排名、进度和短评；如果确实想去 Bangumi 页面，再点弹层里的链接。为了不破坏浏览器习惯，`Ctrl` / `Command` 点击仍然保持直接新标签打开。

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
