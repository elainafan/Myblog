# 音乐歌单同步

播放器读取 `data/music/generated.json`，不要再手动改 `layouts/partials/footer/custom.html` 里的 APlayer `audio` 数组。

## 本地音乐

把音乐放到 `static/music/<歌曲文件夹>/`，至少包含一个音频文件：

```text
static/music/歌曲名/music.mp3
static/music/歌曲名/cover.jpg
```

如果要给本地歌曲补标题和歌手，改 `data/music/local.json`。然后运行：

```powershell
python scripts\sync_music.py local
```

脚本会扫描 `static/music`，重新生成 `data/music/generated.json`。

## Bilibili 收藏夹

先安装 `yt-dlp`：

```powershell
pip install -U yt-dlp
```

当前收藏夹地址已经写在 `data/music/sources.json`，所以可以直接同步：

```powershell
python scripts\sync_music.py bilibili
```

也可以临时指定收藏夹的 `media_id` 或完整 URL：

```powershell
python scripts\sync_music.py bilibili --media-id 你的media_id
python scripts\sync_music.py bilibili --favlist-url "https://space.bilibili.com/502066312/favlist?fid=3416015012&ftype=create"
```

如果收藏夹不是公开的，可以把浏览器里的 Bilibili Cookie 放到环境变量 `BILIBILI_COOKIE`，或者写进本地 cookie 文件后用：

```powershell
python scripts\sync_music.py bilibili --media-id 你的media_id --cookie-file bilibili.cookie.txt
```

脚本会把 Bilibili 音频保存到 `static/music/bilibili/<BV号>/`，并写入 `info.json`。最后它会自动合并本地音乐和 Bilibili 音乐，生成 `data/music/generated.json`。

Bilibili 同步默认保存原始音频格式，通常是 `music.m4a`，不强制转成 mp3，因此不需要额外安装 `ffmpeg`。

第一次测试时可以只同步前几首：

```powershell
python scripts\sync_music.py bilibili --limit 3
```

## 一键合并

```powershell
python scripts\sync_music.py all --media-id 你的media_id
```

`all` 会先同步 Bilibili 收藏夹，再扫描本地音乐目录。
