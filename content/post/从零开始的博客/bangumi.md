---
title: Bangumi 收藏墙
date: 2026-03-13
slug: bangumi-wall
aliases:
    - /p/在博客中优雅地添加bangumi追番页面/
hidden: true
seriesOrder: 3
---

本站的 `/anime/` 最初读取 Bilibili 追番数据，后来整页换成了 Bangumi 收藏。Bilibili 更适合播放，版权、地区和下架状态都会影响条目；Bangumi 的作品信息与个人收藏状态更完整，拿来做长期动画记录更稳。

页面展示公开收藏，数据先同步到本地，再交给 Hugo 渲染。构建过程不请求收藏 API，Bangumi 暂时不可用时，线上已有页面不会变空。

## 同步收藏

公开收藏接口按用户与条目类型查询：

```text
https://api.bgm.tv/v0/users/1020990/collections?subject_type=2&limit=100&offset=0
```

`subject_type=2` 表示动画。接口会返回收藏状态、个人评分、观看进度、短评以及作品封面、放送日期、站内评分和排名。

`scripts/sync_bangumi.py` 负责翻页，并把页面需要的字段写入 `data/bangumi/anime.json`：

```python
DEFAULT_USER = "1020990"
DEFAULT_OUTPUT = Path("data/bangumi/anime.json")

def normalize_item(item):
    subject = item.get("subject") or {}
    return {
        "subject_id": item.get("subject_id"),
        "type": item.get("type"),
        "rate": item.get("rate") or 0,
        "ep_status": item.get("ep_status") or 0,
        "comment": item.get("comment"),
        "subject": {
            "name": subject.get("name"),
            "name_cn": subject.get("name_cn"),
            "date": subject.get("date"),
            "score": subject.get("score"),
            "rank": subject.get("rank"),
            "eps": subject.get("eps") or 0,
            "images": subject.get("images") or {}
        }
    }
```

同步当前用户时运行：

```powershell
python scripts\sync_bangumi.py
```

也可以指定其他公开用户和输出位置：

```powershell
python scripts\sync_bangumi.py --user 用户ID --output data/bangumi/anime.json
```

同步失败时脚本返回非零状态，但不会删除旧 JSON。部署前手动运行，或者在自己的 CI 中定时更新即可；Vercel 只负责读取提交到仓库的数据并构建页面。

## 页面入口

番剧页面位于 `content/page/anime/index.md`：

```yaml
---
title: "番剧 | Anime"
layout: "anime"
slug: "anime"
url: "/anime/"
menu:
    main:
        weight: -50
        params:
            icon: bilibili
---

{{</* bangumi */>}}
```

左侧菜单继续使用原来的 Bilibili 图标，页面内容已经完全由 Bangumi shortcode 生成。`layouts/page/anime.html` 沿用文章容器与评论区，真正的收藏墙在 `layouts/shortcodes/bangumi.html`。

shortcode 只读取本地数据：

```go-html-template
{{- $bangumiData := site.Data.bangumi.anime -}}
{{- $items := $bangumiData.data | default (slice) -}}
```

头部显示收藏总数、最近同步日期和 Bangumi 主页链接。收藏按“在看、看过、想看、搁置、抛弃”拆成独立面板，只生成有内容的状态按钮，不放一个很长的“全部”列表。

## 收藏卡片

卡片默认只保留封面与标题。个人评分、站内评分、排名、观看进度和短评收在悬停层与详情弹窗中，列表不会因为每张卡片塞满文字而变得很长。

面板带有自己的初始数量和展开步长：

```go-html-template
<section
  data-bangumi-panel="{{ .name }}"
  data-bangumi-initial="{{ .initial }}"
  data-bangumi-step="{{ .step }}">
```

`assets/ts/main.ts` 读取这些属性。每次点击 `Load More` 只增加当前状态的显示数量；切换状态后，搜索与展开数量也跟着切到对应面板。

“看过”默认按个人评分降序排列，还可以切到年份视图。年份视图重新排序卡片，并在相邻年份之间动态插入分隔条。没有个人评分的条目自然落在后面，不会和高分收藏混在一起。

普通点击卡片会打开站内详情弹窗，方向键可以切换前后条目，`Esc` 关闭。按住 `Ctrl`、`Command` 或 `Shift` 点击时保留浏览器原行为，仍能直接在新标签页打开 Bangumi 条目。

## 随机一部

“随机一部”并不从个人收藏中抽取。前端向 Bangumi 公共条目接口随机取一段候选数据，再按规则筛选：

```ts
return Boolean(subject.id)
    && year >= 2006
    && (subject.rating?.score || 0) >= 6
    && hasJapaneseKana
    && !BANGUMI_NON_JP_KEYWORDS.test(title)
    && !BANGUMI_SIDE_STORY_KEYWORDS.test(title);
```

这里要求作品从 2006 年开始、站内评分不低于 6、原名包含日文假名，同时排除欧美动画关键词以及 OVA、OAD、ONA、剧场版、特典、总集篇等旁支条目。筛选不是作品国别数据库，只是用公开字段做一层实用过滤，目的是尽量避免抽出蜘蛛侠或一串特典。

页面加载后会提前请求一批候选项。点击按钮时优先从内存池抽取，剩余数量不足再后台补充。请求超过 `1600ms` 或接口失败时，改用本地兜底池；兜底条目同样带封面、年份、评分和可点击链接，因此网络慢时不会只剩一张无图空卡。

## 样式与 PJAX

收藏墙样式随 shortcode 一起输出，作用域限制在 `.bangumi-page`，不会覆盖普通文章卡片。桌面端使用多列封面墙，窄屏逐步减少列数；头部、导航和卡片宽度都由同一个内容容器控制，避免出现头部向里缩、列表却贴边的错位。

交互初始化集中在 `setupBangumiCollection()`，并由 `window.Stack.init()` 调用。直接打开 `/anime/` 和通过 PJAX 切入页面走的是同一套初始化逻辑；根节点用 `data-bangumi-enhanced` 防止重复绑定事件。
