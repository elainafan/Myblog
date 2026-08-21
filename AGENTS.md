# 博客维护指南

## 适用范围

本文件适用于整个仓库。这里是 Elainafan 的 Hugo 博客源码，维护目标依次是：保护已有内容和个人数据、保持现有 URL 与页面行为稳定、完成任务所需的最小改动、留下可复查的验证结果。

默认使用中文沟通和写作。除非任务明确要求，不做全站重排、批量格式化、主题升级、依赖更新、数据刷新、Git 同步或部署。

## 当前维护重点

- 当前阶段不主动新增、续写、重构或美化文章，也不主动调整主题和站点功能。除非用户在新任务中另有明确要求，日常维护只处理 Bangumi 数据同步和音乐歌单同步。
- “同步 Bangumi”只更新 Bangumi 数据及其直接生成结果；“同步歌单”只更新音乐元数据、所需媒体和生成歌单。不要借同步任务顺手修改文章、页面、样式或其他数据。
- 这是当前阶段的维护偏好，不是永久禁止。用户后续的明确指令优先于本节。

## 开始工作前

1. 确认当前目录是本仓库根目录，而不是外层 Hugo 解压目录：

   ```powershell
   git rev-parse --show-toplevel
   git worktree list --porcelain
   git status --short --branch
   ```

2. 记录已有改动。工作区经常保留尚未提交的文章、数据、模板和生成资源；它们都视为用户工作，不得覆盖、还原、暂存或顺手整理。
3. 不要自行执行 `git pull`、`git rebase`、`git checkout`、`git restore`、`git reset`、`git stash`、`git clean`、提交、推送或部署，也不要使用 `git add -A`、`git add .` 或通配路径把整棵工作树收入任务。尤其禁止 `git clean -fdx` 或 `git clean -X`：`.gitignore` 中有一套本地文章和 Cookie，清理 ignored 文件会造成真实数据丢失。
4. 外层工作区可能有 `../.ai-lab-notes/`。它是同仓库的 linked worktree，不是缓存目录或构建沙箱；任务未明确指定时，不要编辑、同步、删除或在其中运行验证，也不要执行会影响它的 `git worktree remove` / `git worktree prune`。
5. 先判断任务属于文章、页面、样式/模板、动态数据还是同步脚本，再阅读目标文件、同目录入口和最近的 2–3 个相邻范例。

## 仓库地图

| 路径 | 作用 | 维护边界 |
| --- | --- | --- |
| `content/post/` | 文章与系列 | 当前主结构是“系列目录 + `main.md` + 子篇 `.md`”，不要擅自迁成一篇一目录的 `index.md` |
| `content/page/` | About、搜索、友链、番剧、图库等独立页面 | 通常使用 `index.md`，并依赖对应 `layout`、`slug` 或 `url` |
| `content/categories/` | 分类页元数据和封面 | 使用 `_index.md`；改名会影响分类 URL 和引用 |
| `hugo.yaml` | 站点、主题、评论、Markdown、KaTeX 与 URL 配置 | 属于全站配置；不要为单篇文章随意修改 |
| `layouts/` | 对 Stack 主题的模板覆盖和 shortcode | 实际站点行为优先看这里，不要只看主题目录 |
| `assets/` | Hugo Pipes 处理的 SCSS、TS、JS、图标、背景和图库素材 | 会由 Hugo 编译；仓库没有独立的 npm 构建流程 |
| `static/` | 原样复制到站点根的图片、音乐和其他文件 | 路径就是公开 URL；大文件改动要单独核对 |
| `data/` | 友圈、音乐、Bangumi、Codeforces 等结构化数据 | 有些是手工源数据，有些由脚本生成，见下文 |
| `scripts/` | 外部数据和文章同步脚本 | 多数会联网并写文件，不能当作无副作用的检查命令 |
| `themes/hugo-theme-stack/` | 仓库内 vendored 的上游主题快照，不是 submodule | 日常定制优先放根级 `layouts/`、`assets/`；除非任务就是同步主题，否则不要改这里 |
| `resources/_gen/` | Hugo 生成并被 Git 跟踪的资源缓存 | 不手改；构建可能批量增删，提交前必须判断是否真有必要 |
| `public/` | 本地构建产物，也是 Vercel 输出目录 | 当前没有被 Git 忽略；不要提交，清理前先确认其中没有人工文件 |
| `vercel.json` | Vercel 构建入口 | 生产命令是 `hugo --gc --minify --cleanDestinationDir` |
| `.github/workflows/update-friends.yml` | 每 3 小时刷新友圈数据 | 当前唯一有效的 Actions workflow，只自动提交 `data/friend_posts.json` |

仓库跟踪了 Windows 版 Hugo Extended；当前快照为 v0.131.0，主题声明的最低版本为 v0.123.0。优先使用 `.\hugo.exe`，并先用 `.\hugo.exe version` 确认实际版本。SCSS 构建依赖 Extended 版本。`.github/workflows/新建 文本文档.txt` 只是未启用的旧 GitHub Pages 配置，扩展名不是 `.yml`/`.yaml`，不要把它当作部署链路。

## 内容结构

### 系列与页面

- `content/post/<系列>/main.md` 是可见的系列入口；同目录子篇通常设置 `hidden: true`，并保留 `seriesOrder`。
- 新增子篇时，同时检查并更新 `main.md` 中的人工目录。站点当前并不依赖 `seriesOrder` 自动生成完整目录。
- `seriesOrder` 可能为负数、不连续或由同步脚本维护。保留它，但不要机械重排。
- `seriesExclude: true` 常见于系列入口。不要在未理解列表过滤逻辑时删除。
- 特殊页面沿用 `content/page/<name>/index.md`；分类页沿用 `content/categories/<name>/_index.md`。
- `.gitignore` 中的 `content/post/从零开始的随机算法/` 是本地保留内容，默认不参与批量修改、统计和提交。任务明确涉及它时，先说明其 ignored 状态。

### Front matter

- 现有内容统一使用 YAML `---`。复制同系列最近的文章作为模板，不要直接套用通用 archetype，也不要批量改成 TOML。
- 保留已有字段、顺序和语义。常见字段包括 `title`、`date`、`categories`、`slug`、`image`、`hidden`、`seriesOrder`、`seriesExclude`、`encrypt`、`aliases`、`layout`、`url`、`comments` 和 `updates`。
- 修改旧文时通常保留原 `date`。只有用户明确要求改变发布日期时才修改。
- `slug` 决定文章的 `/p/:slug/` URL；`url` 会直接覆盖地址。不要随意更改文件名、`slug` 或 `url`，否则内部链接、外部链接和按 URL 映射的 Giscus 评论都可能断开。
- 确需迁移地址时，搜索全部引用并根据相邻建站文章的做法保留 `aliases`。
- `hidden: true` 表示页面仍构建、仍可由链接访问，只是不进入常规列表；它不是草稿。不要自行把 `hidden` 和 `draft` 互换。
- `encrypt` 是逐页开关，不从目录或入口继承；只有 `encrypt: true` 才启用，`false` 明确表示不加密。任何 `true`/`false` 变化都必须由用户明确授权。
- `updates` 只记录已发布文章的实质变更，例如内容、代码、资源、结构或页面行为。普通错别字不记；格式沿用当前文件，通常最新记录在前，说明写简短事实句。

### 内链与资源

- 站内文章链接使用 Hugo `ref`，例如 `[集合]({{< ref "01-sets.md" >}})`；外部链接使用普通 Markdown URL。
- 移动或改名 Markdown 文件前，先用 `rg` 搜索所有 `ref`。不能只改目标文件。
- 系列共享图片通常放在该系列的 `assets/` 下并用相对路径引用；老建站教程也会把 `stack-1.png` 一类图片直接放在同目录。沿用目标系列的现状。
- 站点级或跨文章共享资源放在 `static/images/`，正文和 front matter 以 `/images/...` 引用。
- 已公开并提供给外站的静态资源 URL 视为长期接口。改名或迁移前必须保留旧路径的兼容副本或重定向；仓库内搜索不到引用不能证明外部站点已经停止使用，未经用户明确授权不得直接删除旧路径。
- 头像更新时同时替换 `assets/img/elainafan.jpg`、`static/avatars/elainafan.jpg` 和兼容路径 `static/avatars/elaniafan.jpg`，并确认三份内容一致。侧栏与默认 Open Graph 图读取 `assets` 文件；本站对外提供的规范友链头像地址始终使用 `https://www.elainafan.one/avatars/elainafan.jpg`，两个 `static` 路径都必须可访问。
- 不批量移动、重命名或重新压缩旧图片。新增图片应有能说明内容的 alt 文本，并确认大小写与真实文件名一致。
- `static/music/` 当前已有约 600 MiB 的已跟踪音频资源。不要把一次普通文章改动扩展成媒体批量变更；同步后只按预期目录精确审查和暂存。

## 写作与 Markdown

- 默认写清楚、直接、便于以后复习的中文笔记。技术名词可以自然使用英文，例如 `input`、`debug`、`Lab`、`kernel` 和 `Rating`。
- 每句话应提供事实、定义、机制、约束、实现、结果、限制或真实个人观察。删去空泛的预告、重复总结和只负责“提醒重点”的句子。
- 不编造个人经历、日期、耗时、成绩、比赛结果、实验输出、Cookie、地址或观点。目标是可发布成稿时，缺失事实应询问用户或省略；只有明确的草稿、提纲或任务笔记可以保留占位。
- 正文通常从 `##` 开始，因为页面标题来自 front matter。部分旧 Lab 和练习笔记保留正文 `#`；编辑旧文时跟随邻篇，不做全站清洗。
- 代码块写语言标记；命令必须可复制。旧文章中的双反引号、局部措辞和归档格式可以保留，不要为统一风格制造大 diff。
- 新增或补写比赛日志时保持“题目/出处、题意、数据范围、思路、代码”的紧凑结构；约束要和算法选择对应。旧归档只改任务触及部分，不为统一结构整篇重写。
- Lab 文章保留声明、环境/测试命令、失败模式和危险操作警告；不要弱化原有的防抄袭提示。
- 课程与推导笔记从定义、对象或例子开始，按真实逻辑展开，不强行添加“核心思想”和结尾总结。日常、动漫和 Rating 总结可以更温暖、个人化，但仍不能编造经历或观点。
- 行内 KaTeX 公式与中文及标点之间留空格；展示公式独占块并在前后留空行。LaTeX 命令使用单反斜杠，源码中的公式换行使用四个反斜杠 `\\\\`。只修本次触及的公式，不批量清理旧文。
- `hugo.yaml` 已启用 Goldmark unsafe HTML 和公式 passthrough。除非任务要求，不要靠改全局 Markdown 配置来修一篇文章。

## 站点定制

根级模板与资源已经大幅覆盖 Stack 主题，功能往往横跨多处：

| 功能 | 主要入口 | 数据或相关文件 |
| --- | --- | --- |
| 全站外观、文章、归档、搜索 | `layouts/`、`assets/scss/`、`assets/ts/main.ts` | `hugo.yaml` |
| PJAX、KaTeX、Giscus、运行时间、加密交互 | `layouts/partials/footer/custom.html` | `layouts/partials/article/components/content.html`、`assets/scss/custom/` |
| 音乐播放器 | `assets/js/music-player.js`、`assets/scss/music-player.scss` | `data/music/`、`static/music/`、`scripts/sync_music.py` |
| Bangumi 页面 `/anime/` | `content/page/anime/index.md`、`layouts/page/anime.html`、`layouts/shortcodes/bangumi.html` | `data/bangumi/anime.json`、`scripts/sync_bangumi.py` |
| 友链与友圈 `/friends/` | `content/page/link/index.md`、`layouts/partials/article/components/friend-circle.html` | `data/friends.yaml`、`data/friend_posts.json`、`scripts/fetch_friend_feeds.py` |
| 图库 `/photos/` | `content/page/photo/index.md`、`layouts/photo/single.html` | `assets/waifus/`、`scripts/import_photos.py` |
| 文章图片预览 | `layouts/_default/_markup/render-image.html` | Page Resources、`static/images/`、PhotoSwipe |
| 比赛日记 | `content/post/二次元修炼日记！/` | `data/codeforces.yaml` 与多个 `sync_*official.py` / `sync_contest_diaries.py` |

修改这些功能时遵守以下规则：

- Hugo 的覆盖优先级是根级 `layouts/`、`assets/` 高于 `themes/hugo-theme-stack/`。先找实际生效的覆盖文件，避免同时修改两份实现。
- 根级覆盖即使与当前主题内容相同，也会遮蔽将来的上游修复。禁止整目录把新版主题复制到根级 `layouts/` / `assets/`，也禁止用主题目录反向覆盖根级定制；主题升级必须逐文件做三方比对。
- 仓库没有 `package.json`。TypeScript 和 SCSS 由 Hugo Pipes 处理，不要为了小改动引入一套新的前端构建链。
- 本站使用 PJAX。需要在换页后生效的代码不能只监听首次加载；同时考虑 `pjax:complete`，并保证重复初始化不会叠加 DOM、播放器、评论框或事件监听器。
- 样式改动至少检查桌面/移动端、浅色/深色。交互改动要连续导航多次并测试浏览器前进后退。
- 加密仅是现有的客户端访问交互，正文仍会进入生成的 HTML，不能保护真正私密的内容。不要在任务外更改密码派生、散列、角色素材或解锁逻辑，也不要把私密原文、凭据或 Cookie 写入仓库。
- 外部 CDN、API 与评论服务会影响运行时。替换或移除前先确认离线构建、PJAX 重载和失败回退行为。

## 数据与脚本

运行任何同步脚本前先阅读其参数、默认输入和写入路径。联网刷新属于数据变更，不是常规验证步骤。

### Bangumi

- 使用 `python scripts\sync_bangumi.py` 从 Bangumi API 刷新收藏，默认覆盖 `data/bangumi/anime.json`。不要为一次数据刷新改动 `/anime/` 页面模板或样式。
- 同步前后比较 `data/bangumi/anime.json`，确认用户、条目数、收藏状态、评分和时间字段没有异常。用 `python -m json.tool data\bangumi\anime.json` 检查 JSON，再按需做 Hugo 快速构建。

### 音乐歌单

- 音乐以 `data/music/local.json` 和 `data/music/sources.json` 为源，播放器读取生成的 `data/music/generated.json`。具体流程见 `scripts/README-music.md`。不要手改模板中的播放列表。
- Bilibili 视频标题和 UP 主名称不等于可靠的歌曲元数据。每次同步后都要人工检查新增曲目，并在 `data/music/local.json` 用完整 `folder` 覆盖 `name` 和 `artist`；该文件中的人工元数据优先。
- 歌名规范：全英文标题保留英文；日文标题只要含有汉字，就保留日文原名；全为假名、没有汉字的日文标题翻译成中文。不要把保留原名理解成罗马字转写，也不要为了套规则批量重写旧歌名。
- 歌手规范：不要把 UP 主默认当作歌手。优先使用真实演唱者；角色歌或动画内由角色演唱、角色身份更有意义时，使用作品中的角色名。
- 分 P 不能一刀切。脚本默认同步一个 BVID 的全部分 P，但 `scripts/sync_music.py` 的 `BILIBILI_PAGE_SELECTION` 可以为特定 BVID 指定保留页；是否保留 P2 及后续页要按实际歌曲内容判断。
- `BV1MW4y1S7nL`（天津四与角宿一）和 `BV13a411H7mU`（两人的匹诺曹）只保留 P1，不要同步 P2。
- `BV1chikYJEMZ`（轻音合集）只保留 P1、P2、P3、P4、P12、P19、P20，即 `Cagayake! GIRLS`、`Don't Say Lazy`、澪版和唯版 `ふわふわ時間`、`No, Thank You!`、`五月雨20ラブ`、`Singing!`；明确排除 P21 破音版及其他分 P。
- 其他已知需保留全部分 P 的投稿包括 `BV1K2421F737`（春物 OP 合集，P1–P3）和 `BV1Q2421M7pf`（春物 ED 合集，P1–P3）。遇到新的多 P 投稿时先检查每一 P；无法判断就停止并向用户确认 `BVID → 保留哪些 P`，不得猜测后直接运行非 dry-run 同步。
- `BILIBILI_EXCLUDED_VIDEOS` 保存“收藏夹中即使存在也不要进入本地歌单”的投稿；当前 `BV1Ns411M7TG`（`Step by Step Up`）必须排除。删除这类歌曲时同步更新该集合，否则下次抓取会重新下载。
- `scripts/sync_music.py` 的 Bilibili 模式会调用 `yt-dlp`、下载媒体并改写 `static/music/bilibili/` 与生成数据；非 dry-run 还会清理未包含在本次列表中的旧曲目。小范围探查只能把 `--limit` 与 `--dry-run` 联用：单独使用 `--limit` 会把截断范围外的现有曲目当作 stale 删除。dry-run 仍会重写 `data/music/generated.json`，所以同样要先记录状态并审查 diff。不要随意使用 `--force`。
- 私有 Bilibili Cookie 只放在环境变量或被忽略的 `bilibili.cookie.txt`。不得打印、提交或复制到文章、日志和交接说明中。

### 其他同步

- 当前阶段不要主动运行朋友圈、图库、Codeforces、AtCoder 或 contest diary 同步；只有用户明确提出对应任务时才执行。
- `scripts/fetch_friend_feeds.py` 从 `data/friends.yaml` 生成 `data/friend_posts.json`；GitHub Actions 也会自动刷新后者。人工编辑抓取结果很可能被覆盖。
- `scripts/import_photos.py` 会下载并写入 `assets/waifus/`，依赖 Pillow；`--clear` 会先删除现有图库，未经明确授权不要运行。
- Codeforces、AtCoder 和 contest diary 同步脚本会同时改数据、系列入口和多篇 Markdown。默认路径分别可能指向仓库外的 `D:\code\CP\Codeforces`、`D:\code\CP\Atcoder` 和 `D:\code\Contests`；AtCoder 脚本还依赖 Windows `curl.exe`。先核实当前机器路径、账号和变更范围，再运行。
- `scripts/sync_codeforces_official.py` 没有真正的 CLI 参数解析；给它传 `--help` 仍会联网并执行写入，不能用这种方式探查。
- 同步后必须审查 `git diff --stat` 和每类生成文件。源数据、脚本与必要生成结果应作为同一逻辑改动交接；不要混入无关缓存或媒体。

## 预览、构建与验证

本地预览优先使用：

```powershell
.\hugo.exe server -D --disableFastRender --renderToMemory --noBuildLock
```

不启动服务器的快速构建检查可使用：

```powershell
.\hugo.exe --renderToMemory --noBuildLock --minify
```

`--renderToMemory` 只避免写入 `public/`，`--noBuildLock` 只避免写构建锁；Hugo Pipes 仍可能更新被跟踪的 `resources/_gen/`。预览和快速构建也必须在前后比较 `git status --short`。

与 `vercel.json` 参数一致的本地生产构建为：

```powershell
.\hugo.exe --gc --minify --cleanDestinationDir
```

生产命令会清理 `public/`，`--gc` 也可能改变被跟踪的 `resources/_gen/`。运行前后都要保存并比较 `git status --short`。工作区已有生成资源改动时，不要复用 `../.ai-lab-notes/`，也不要自行创建、删除或清理 worktree；确需隔离构建时先与用户确认方案。绝不能为了得到“干净状态”而还原用户原有改动。

`vercel.json` 只能证明构建命令和 `public/` 输出目录；Vercel 的 Hugo 版本、Git 连接、触发分支和当前线上状态没有在仓库内声明，不能据此推断部署已经发生。

按改动类型验证：

- 只改文章：确认 Hugo 无新增 ERROR，检查目标页面、目录链接、图片、代码块和公式。
- 改 front matter 或路径：检查最终 URL、`ref`、系列入口、分类/归档可见性与旧地址兼容。
- 改模板/样式：检查首页、列表页、普通文章、长文、搜索页及相关特殊页面，并覆盖移动端和深色模式。
- 改 PJAX/播放器/评论/公式/加密：从一个页面连续跳到另一个页面，使用前进后退，再确认组件只初始化一次且控制台无新增错误。
- 改 JSON：可用 `python -m json.tool data\bangumi\anime.json` 这类命令做语法检查，再执行 Hugo 构建。
- 改 Python：先做无写入的 AST 语法检查，例如 `python -c "import ast,pathlib; ast.parse(pathlib.Path(r'scripts\sync_bangumi.py').read_text(encoding='utf-8'))"`；只有确认 `--help` 不会触发主流程时才用它探查参数。

结束前至少执行：

```powershell
git status --short
git diff --check -- AGENTS.md
git diff -- AGENTS.md
Get-Content -LiteralPath 'AGENTS.md' -Encoding utf8
```

上面以 `AGENTS.md` 为示例；实际任务应把路径换成本次触及的文件，逐项检查。前两个 `git diff` 命令用于已跟踪文件，直接读取用于核对新文件的完整内容。

未跟踪的新文件不会出现在普通 `git diff` 中；还应在 `git status` 中确认它，或使用 `git diff --no-index -- /dev/null AGENTS.md` 这类命令审阅。该命令发现差异时退出码为 1，这是正常结果。

不要把仓库原有警告或未执行的人工浏览器测试描述成“已通过”。构建产生的 `public/`、`resources/_gen/` 或锁文件变化必须显式说明，并从本次提交范围中排除，除非任务明确需要它们。

## 交接格式

完成任务时给出：

- 改了什么，以及用户可见行为是否变化；
- 实际修改的文件；
- 执行过的验证命令和结果；
- 未执行的验证及原因；
- 生成数据、外部服务、浏览器人工检查或部署方面的剩余风险；
- 工作前已经存在、且本次没有触碰的相关改动。

未经用户明确要求，不提交、不推送、不创建 PR、不触发部署。不要声称 Vercel 已上线，除非确实检查了对应部署结果。
