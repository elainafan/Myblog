---
title: 音乐播放器与 PJAX
date: 2026-05-20
slug: music-player
aliases:
    - /p/在博客中优雅地引入音乐播放器/
hidden: true
seriesOrder: 2
---

播放器最早使用 APlayer，后来换成了原生 `Audio` 和一套自己的悬浮界面。这样可以控制面板尺寸、播放模式、歌单展开方式和移动端布局，也不必再覆盖几百行第三方播放器样式。

页面切换仍由 PJAX 完成。播放器常驻在被替换区域之外，点进下一篇文章时不会重新创建 `Audio`，歌曲和进度都能接着播放。

## 悬浮播放器

Hugo 只负责把生成后的歌单交给浏览器。入口位于 `layouts/partials/footer/custom.html`：

```go-html-template
<script>
  window.__ELAINA_MUSIC_PLAYLIST__ =
    {{ .Site.Data.music.generated | default (slice) | jsonify | safeJS }};
</script>

{{ with resources.Get "js/music-player.js" }}
<script src="{{ .RelPermalink }}" defer></script>
{{ end }}
```

播放器实现放在 `assets/js/music-player.js`，样式放在 `assets/scss/music-player.scss`。脚本创建一个原生 `Audio`，再按歌单数据生成封面、曲名、歌手、进度条和控制按钮。页面中没有固定的播放器 HTML，初始化时才插入：

```js
const audio = new Audio();
audio.preload = 'metadata';

const root = document.createElement('section');
root.id = 'elaina-music-player';
root.className = 'music-player';
document.body.append(root);
```

底部只显示当前曲目和常用控制，点击封面或列表图标后展开完整歌单。按钮使用 SVG 图标并带有 `title` 与 `aria-label`，不会用一排长文字挤占播放器宽度。

播放顺序分为列表循环、随机播放和单曲循环：

```js
const PLAYBACK_MODES = ['list', 'random', 'repeat-one'];
```

歌曲自然播放结束时，单曲循环会重新载入当前曲目；随机模式会避开当前索引；列表模式顺序移动并在末尾回到开头。手动点下一首时不会被单曲循环拦住。

## 保存播放状态

播放器状态写入 `localStorage`，键名为 `elainaMusicPlayerState`。目前保留曲目索引、播放时间、暂停状态、音量、面板展开状态和播放模式：

```js
localStorage.setItem('elainaMusicPlayerState', JSON.stringify({
    index: currentIndex,
    currentTime: audio.currentTime,
    paused: audio.paused,
    volume: audio.volume,
    expanded: isExpanded,
    mode: playbackMode
}));
```

恢复进度不能在设置 `src` 后立刻写 `currentTime`。音频元数据尚未加载时，浏览器还不知道总时长。脚本先把位置存在 `pendingSeek`，等 `loadedmetadata` 再跳转：

```js
audio.addEventListener('loadedmetadata', () => {
    if (pendingSeek > 0 && Number.isFinite(audio.duration)) {
        audio.currentTime = Math.min(
            pendingSeek,
            Math.max(audio.duration - 0.25, 0)
        );
    }
    pendingSeek = 0;
});
```

状态会在播放、暂停、拖动进度、切歌、切换模式和关闭页面时更新。PJAX 切页不会销毁播放器，因此正常站内跳转甚至不需要恢复；`localStorage` 主要负责整页刷新和重新打开浏览器后的续播。

## 生成歌单

实际播放数据是 `data/music/generated.json`，由 `scripts/sync_music.py` 生成。本地歌曲放在 `static/music`，每首歌一个目录：

```text
static/music/歌曲目录/
├── music.mp3
├── cover.jpg
└── info.json
```

支持的音频扩展名包括 `mp3`、`m4a`、`ogg`、`flac` 和 `wav`。只扫描本地目录时运行：

```powershell
python scripts\sync_music.py local
```

歌单也可以从 Bilibili 收藏夹同步。收藏夹地址写在 `data/music/sources.json`，脚本读取公开列表，再调用 `yt-dlp` 下载音频与封面：

```powershell
python scripts\sync_music.py bilibili --media-id 收藏夹ID
```

分 P 视频会保存到独立的 `p01`、`p02` 目录。少数视频只有 P1 是需要的歌曲，例如《继母的拖油瓶是我的前女友》的 OP 与 ED；这类 BV 号列在 `BILIBILI_FIRST_PAGE_ONLY` 中，后续分 P 不会进入歌单。

Bilibili 标题不适合直接当歌曲元数据。`data/music/local.json` 用来覆盖生成结果中的 `name` 和 `artist`。本站采用的命名规则是“曲名 + 演唱者”：曲名含汉字或全英文时保留原名，全是假名时再翻译；角色曲可以使用作品中的角色名，例如由比滨结衣。

同步脚本会删除已经离开收藏夹的旧下载目录，然后重新生成 JSON。播放器本身只读站内静态文件，访问者打开页面时不会请求 Bilibili。

## PJAX 切页

PJAX 由 `layouts/partials/footer/custom.html` 初始化，只替换正文容器、评论区域和运行时间区域。播放器挂在 `body` 下并位于这些选择器之外，所以切页期间保持原对象和当前音频流。

```js
const pjax = new Pjax({
    selectors: ['.main-container', '.js-Pjax', '.Timer'],
    cacheBust: false
});
```

PJAX 返回的新页面可能有不同的 `body` class。请求完成前先用 `DOMParser` 解析响应，把新页面的 class 同步到当前 `body`；否则文章页、搜索页和独立功能页会沿用上一个页面的布局状态。

切页库还会把时间戳写进 URL。本站的清理函数同时处理普通查询参数和锚点后的查询串，避免出现 `#标题?t=...`：

```js
function cleanPjaxTimestamp(rawUrl) {
    const url = new URL(rawUrl, window.location.origin);
    url.searchParams.delete('t');

    if (url.hash.includes('?')) {
        const [anchor, query] = url.hash.split('?');
        const params = new URLSearchParams(query);
        params.delete('t');
        url.hash = params.toString() ? `${anchor}?${params}` : anchor;
    }
    return url.toString();
}
```

`pjax:complete` 之后不只要隐藏顶部进度条。新正文中的图片、代码块、目录、搜索、KaTeX 和 Bangumi 控件都需要重新绑定：

```js
document.addEventListener('pjax:complete', () => {
    const cleanUrl = cleanPjaxTimestamp(window.location.href);
    if (cleanUrl !== window.location.href) {
        history.replaceState(null, '', cleanUrl);
    }

    renderKaTeX();
    window.Stack.init();
    topbar.hide();
    playArticleEntryMusic();
});
```

PhotoSwipe 的依赖放在常驻 footer，`window.Stack.init()` 只扫描新的 `.article-content`。Giscus 则不能复用旧 iframe，脚本会在新页面存在 `.comment` 时重新注入，并根据当前明暗模式设置主题。运行时间和访问量同样在 PJAX 完成后刷新。

## 文章联动

算法文章可以在进入页面时随机播放 `Magia` 或 `Everyday World`。模板在满足条件的文章上写入标记：

```go-html-template
<article
  class="main-article"
  data-page-key="{{ .RelPermalink }}"
  data-entry-music="algorithm-random">
```

`assets/js/music-player.js` 读取这个标记，并从两首候选曲中随机选择。若当前已经在播放其中一首，脚本直接返回，不切歌、不归零，也不改变暂停状态：

```js
if (isAlgorithmEntryTrack(currentIndex)) {
    return;
}
```

操作系统、程序设计实习和数算系列已经从这条规则中排除。其余页面没有 `data-entry-music`，普通切页只会保留当前歌曲。
