#!/usr/bin/env python3
"""
Build the site music playlist from local folders and, optionally, a Bilibili
favorite list.

Examples:
  python scripts/sync_music.py local
  python scripts/sync_music.py bilibili --media-id 123456789
  python scripts/sync_music.py bilibili --favlist-url "https://space.bilibili.com/.../favlist?fid=123456789"
  python scripts/sync_music.py all --media-id 123456789
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from contextlib import contextmanager
from pathlib import Path
from typing import Any, NamedTuple


ROOT = Path(__file__).resolve().parents[1]
STATIC_MUSIC = ROOT / "static" / "music"
LOCAL_META = ROOT / "data" / "music" / "local.json"
GENERATED_PLAYLIST = ROOT / "data" / "music" / "generated.json"
SOURCES_CONFIG = ROOT / "data" / "music" / "sources.json"
BILIBILI_MUSIC = STATIC_MUSIC / "bilibili"

AUDIO_NAMES = ("music.mp3", "music.m4a", "music.ogg", "music.flac", "music.wav")
AUDIO_EXTS = (".mp3", ".m4a", ".ogg", ".flac", ".wav")
COVER_NAMES = ("cover.jpg", "cover.jpeg", "cover.png", "cover.webp", "music.jpg", "music.png")
BILIBILI_REFERER = "https://www.bilibili.com/"
BILIBILI_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)
BILIBILI_PAGE_SELECTION = {
    # 継母の連れ子が元カノだった OP / ED. These uploads are multi-part
    # videos, but only P1 is the actual track needed by the playlist.
    "BV1MW4y1S7nL": {1},
    "BV13a411H7mU": {1},
    # K-ON!: eligible tracks; explicit exclusions below take precedence.
    # The intentionally broken-vocal P21 version is never selected.
    "BV1chikYJEMZ": {1, 2, 3, 4, 12, 19, 20},
}
BILIBILI_EXCLUDED_VIDEOS = {
    # NEW GAME! OP. Keep it out of the local playlist even if it remains in
    # the Bilibili favorite list.
    "BV1Ns411M7TG",
    "BV15k4y1m7zb",  # 厘米 / センチメートル
    "BV1ab411S7UV",  # SAVE MY HEART
    "BV1du4m1u7rL",  # 夢の続き
    "BV15NbN6jEM3",  # 梦想世界
}
BILIBILI_EXCLUDED_PAGES = {
    "BV1chikYJEMZ": {
        1,   # Cagayake! GIRLS
        4,   # ふわふわ時間（唯版）; keep the Mio version at P3.
        19,  # 五月雨20ラブ
    },
    "BV1Q2421M7pf": {
        1,  # Hello Alone
        3,  # ダイヤモンドの純度; keep Everyday World at P2.
    },
}


def is_bilibili_track_excluded(bvid: str, page: int) -> bool:
    return bvid in BILIBILI_EXCLUDED_VIDEOS or page in BILIBILI_EXCLUDED_PAGES.get(bvid, set())

# Bilibili titles are video titles, not reliable song metadata. After each sync,
# add overrides in data/music/local.json so the player shows song title + singer:
# keep titles with kanji/Chinese characters or all-English titles as-is; translate
# all-kana titles to Chinese; use in-anime character names when they are the
# meaningful vocalist identity.


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Replace the old index only after the whole JSON file has been written.
    with tempfile.TemporaryDirectory(dir=path.parent) as temp:
        pending = Path(temp) / path.name
        pending.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        pending.replace(path)


def load_music_overrides() -> dict[str, dict[str, Any]]:
    local_entries = load_json(LOCAL_META, [])
    return {
        entry["folder"]: entry
        for entry in local_entries
        if isinstance(entry, dict) and entry.get("folder")
    }


def url_for_static_file(path: Path) -> str:
    rel = path.relative_to(STATIC_MUSIC).parts
    encoded = "/".join(urllib.parse.quote(part) for part in rel)
    return f"/music/{encoded}"


def first_existing(directory: Path, names: tuple[str, ...]) -> Path | None:
    for name in names:
        path = directory / name
        if path.exists():
            return path
    return None


def find_audio(directory: Path) -> Path | None:
    preferred = first_existing(directory, AUDIO_NAMES)
    if preferred:
        return preferred
    for path in sorted(directory.iterdir()):
        if path.is_file() and path.suffix.lower() in AUDIO_EXTS:
            return path
    return None


def find_cover(directory: Path) -> Path | None:
    preferred = first_existing(directory, COVER_NAMES)
    if preferred:
        return preferred
    for path in sorted(directory.iterdir()):
        if path.is_file() and path.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            return path
    return None


def folder_key(path: Path) -> str:
    return path.relative_to(STATIC_MUSIC).as_posix()


def discover_track(directory: Path, overrides: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    audio = find_audio(directory)
    if not audio:
        return None

    key = folder_key(directory)
    info = load_json(directory / "info.json", {})
    info.update(overrides.get(key, overrides.get(directory.name, {})))

    if is_bilibili_track_excluded(info.get("bvid", ""), int(info.get("page") or 1)):
        return None

    cover = find_cover(directory)
    track = {
        "name": info.get("name") or directory.name,
        "artist": info.get("artist") or "未知艺术家",
        "url": info.get("url") or url_for_static_file(audio),
        "cover": info.get("cover") or (url_for_static_file(cover) if cover else ""),
        "source": info.get("source") or ("bilibili" if "bilibili" in directory.parts else "local"),
    }

    for key in ("bvid", "page", "sourceUrl"):
        if info.get(key):
            track[key] = info[key]

    return track


def build_playlist(exclude: set[Path] | None = None) -> list[dict[str, Any]]:
    exclude = exclude or set()
    local_entries = load_json(LOCAL_META, [])
    overrides = load_music_overrides()

    seen_dirs: set[Path] = set()
    tracks: list[dict[str, Any]] = []

    for entry in local_entries:
        folder = entry.get("folder") if isinstance(entry, dict) else None
        if not folder:
            continue
        directory = STATIC_MUSIC / folder
        if directory in exclude:
            continue
        track = discover_track(directory, overrides) if directory.exists() else None
        if track:
            tracks.append(track)
            seen_dirs.add(directory.resolve())

    for directory in sorted(path for path in STATIC_MUSIC.rglob("*") if path.is_dir()):
        if directory in exclude or directory.resolve() in seen_dirs:
            continue
        track = discover_track(directory, overrides)
        if track:
            tracks.append(track)

    return tracks


def write_playlist(exclude: set[Path] | None = None) -> None:
    playlist = build_playlist(exclude)
    write_json(GENERATED_PLAYLIST, playlist)
    print(f"Generated {GENERATED_PLAYLIST.relative_to(ROOT)} with {len(playlist)} tracks.")


def resolve_media_id(args: argparse.Namespace) -> str:
    if args.media_id:
        return args.media_id
    if args.favlist_url:
        query = urllib.parse.parse_qs(urllib.parse.urlparse(args.favlist_url).query)
        media_id = query.get("fid", query.get("media_id", [""]))[0]
        if media_id:
            return media_id
    sources = load_json(SOURCES_CONFIG, {})
    bilibili = sources.get("bilibili", {}) if isinstance(sources, dict) else {}
    if bilibili.get("media_id"):
        return str(bilibili["media_id"])
    if bilibili.get("favlist_url"):
        query = urllib.parse.parse_qs(urllib.parse.urlparse(bilibili["favlist_url"]).query)
        media_id = query.get("fid", query.get("media_id", [""]))[0]
        if media_id:
            return media_id
    raise ValueError("missing --media-id or --favlist-url with fid")


def http_get_json(url: str, cookie: str | None = None) -> dict[str, Any]:
    headers = {
        "User-Agent": BILIBILI_USER_AGENT,
        "Referer": BILIBILI_REFERER,
    }
    if cookie:
        headers["Cookie"] = cookie
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def load_cookie(args: argparse.Namespace) -> str | None:
    if args.cookie:
        return args.cookie
    if args.cookie_file:
        return Path(args.cookie_file).read_text(encoding="utf-8").strip()
    return os.environ.get("BILIBILI_COOKIE")


def fetch_bilibili_favorite(media_id: str, cookie: str | None) -> list[dict[str, Any]]:
    medias: list[dict[str, Any]] = []
    page = 1
    total = None
    seen = set()
    while True:
        query = urllib.parse.urlencode({"media_id": media_id, "pn": page, "ps": 20})
        payload = http_get_json(f"https://api.bilibili.com/x/v3/fav/resource/list?{query}", cookie)
        if payload.get("code") != 0:
            raise RuntimeError(f"Bilibili favorites API error: {payload.get('message')}")

        data = payload.get("data") or {}
        count = (data.get("info") or {}).get("media_count")
        if not isinstance(count, int) or count < 0 or (total is not None and count != total):
            raise RuntimeError("Missing or changing favorite count; please retry.")
        total = count
        batch = data.get("medias")
        if batch is None and total == 0:
            batch = []
        if not isinstance(batch, list) or not isinstance(data.get("has_more"), bool):
            raise RuntimeError("Incomplete favorite list response.")
        for media in batch:
            key = (media.get("type"), media.get("id") or media.get("bvid"))
            if not key[1] or key in seen or (media.get("type") == 2 and not media.get("bvid")):
                raise RuntimeError("Incomplete or overlapping favorite pages; please retry.")
            seen.add(key)
        medias.extend(batch)
        if not data["has_more"]:
            break
        if not batch or len(medias) >= total:
            raise RuntimeError("Inconsistent favorite pagination; please retry.")
        page += 1
        time.sleep(0.4)

    if len(medias) != total:
        raise RuntimeError(f"Received {len(medias)} of {total} favorites; please retry.")

    return medias


def safe_name(value: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value)
    return value.strip(" .") or "unknown"


def download_file(url: str, target: Path) -> None:
    headers = {"User-Agent": BILIBILI_USER_AGENT, "Referer": BILIBILI_REFERER}
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
        with target.open("wb") as out:
            shutil.copyfileobj(response, out)
        length = response.headers.get("Content-Length")
    size = target.stat().st_size
    if not size or (length is not None and size != int(length)):
        raise OSError(f"Incomplete download: {target.name}")


def has_audio(directory: Path) -> bool:
    return directory.is_dir() and find_audio(directory) is not None


def fetch_bilibili_pages(bvid: str, cookie: str | None) -> list[dict[str, Any]]:
    query = urllib.parse.urlencode({"bvid": bvid})
    payload = http_get_json(f"https://api.bilibili.com/x/player/pagelist?{query}", cookie)
    pages = payload.get("data")
    if payload.get("code") != 0 or not isinstance(pages, list) or not pages:
        raise RuntimeError(f"Missing page list for {bvid}: {payload.get('message')}")
    if [p.get("page") for p in pages] != list(range(1, len(pages) + 1)) or any(not p.get("cid") for p in pages):
        raise RuntimeError(f"Incomplete page list for {bvid}.")
    return pages


def yt_dlp_command(executable: str, page_url: str, output: Path) -> list[str]:
    return [
        executable,
        "-f",
        "bestaudio/best",
        "--no-playlist",
        "--referer",
        BILIBILI_REFERER,
        "--user-agent",
        BILIBILI_USER_AGENT,
        "-o",
        str(output),
        page_url,
    ]


def bilibili_track_directory(bvid: str, page_count: int, page: int) -> Path:
    bvid_dir = BILIBILI_MUSIC / safe_name(bvid)
    if page_count <= 1:
        return bvid_dir
    return bvid_dir / f"p{page:02d}"


class BilibiliTrack(NamedTuple):
    directory: Path
    cid: int
    cover_url: str
    info: dict[str, Any]


def read_track_plan(medias: list[dict[str, Any]], cookie: str | None) -> list[BilibiliTrack]:
    overrides = load_music_overrides()
    tracks = []
    for media in medias:
        bvid = media.get("bvid")
        if not bvid or bvid in BILIBILI_EXCLUDED_VIDEOS:
            continue
        title = media.get("title") or bvid
        pages = fetch_bilibili_pages(bvid, cookie)
        if media.get("page") and len(pages) != media["page"]:
            raise RuntimeError(f"Part count changed for {bvid}; please retry.")
        selected = BILIBILI_PAGE_SELECTION.get(bvid)
        if selected is not None and not selected.issubset({p["page"] for p in pages}):
            raise RuntimeError(f"Missing selected part for {bvid}.")
        for part in pages:
            page = part["page"]
            if (selected is not None and page not in selected) or is_bilibili_track_excluded(bvid, page):
                continue
            # Historically uploads explicitly limited to P1 use the parent folder.
            # For any other selected part preserve its real pNN path and ?p=N URL.
            count = 1 if selected == {1} else len(pages)
            directory = bilibili_track_directory(bvid, count, page)
            page_url = f"https://www.bilibili.com/video/{bvid}"
            if count > 1:
                page_url += f"?p={page}"
            info = {
                "name": (part.get("part") or title) if count > 1 else title,
                "artist": (media.get("upper") or {}).get("name") or "Bilibili",
                "source": "bilibili", "bvid": bvid, "page": page, "sourceUrl": page_url,
            }
            override = overrides.get(folder_key(directory), overrides.get(directory.name, {}))
            for key in ("name", "artist"):
                info[key] = override.get(key) or info[key]
            tracks.append(BilibiliTrack(directory, part["cid"], media.get("cover") or "", info))
    return tracks


def fetch_public_audio(track: BilibiliTrack, target: Path) -> None:
    # Request the public DASH audio for the exact part. Cookies are never sent to media hosts.
    bvid = track.info["bvid"]
    query = urllib.parse.urlencode({"bvid": bvid, "cid": track.cid, "fnval": 16})
    data = http_get_json(f"https://api.bilibili.com/x/player/playurl?{query}")
    if data.get("code") != 0:
        raise RuntimeError(f"Public audio unavailable for {bvid}: {data.get('message')}")
    formats = ((data.get("data") or {}).get("dash") or {}).get("audio") or []
    audio = max((f for f in formats if (f.get("mimeType") or f.get("mime_type")) == "audio/mp4"),
                key=lambda f: f.get("bandwidth", 0), default=None)
    if not audio:
        raise RuntimeError(f"No public M4A audio for {bvid} P{track.info['page']}.")
    urls = [audio.get("baseUrl") or audio.get("base_url")]
    urls.extend(audio.get("backupUrl") or audio.get("backup_url") or [])
    for url in urls:
        if not url:
            continue
        try:
            download_file(url, target)
            with target.open("rb") as f:
                if b"ftyp" not in f.read(64):
                    raise OSError("Invalid M4A response")
            return
        except OSError:
            continue
    raise RuntimeError(f"Could not download the public audio for {bvid} P{track.info['page']}.")


def download_audio(track: BilibiliTrack, staging: Path, executable: str) -> None:
    command = yt_dlp_command(executable, track.info["sourceUrl"], staging / "music.%(ext)s")
    try:
        result = subprocess.run(command, stderr=subprocess.PIPE, text=True, errors="replace")
    except FileNotFoundError:
        result = None
    if result is not None and result.returncode == 0:
        if not has_audio(staging):
            raise RuntimeError(f"No supported audio saved for {track.info['bvid']}.")
        return
    if result is not None and "412" not in result.stderr:
        raise RuntimeError(f"yt-dlp failed for {track.info['bvid']} P{track.info['page']} (exit {result.returncode}).")
    print(f"Trying the public audio stream for {track.info['bvid']} P{track.info['page']}.")
    fetch_public_audio(track, staging / "music.m4a")


def stale_tracks(expected: set[Path]) -> list[Path]:
    return sorted(directory for directory in BILIBILI_MUSIC.rglob("*")
                  if directory not in expected and not directory.is_symlink() and has_audio(directory))


def remove_stale(directory: Path) -> None:
    for path in directory.iterdir():
        if path.is_file() and (path.suffix.lower() in AUDIO_EXTS or path.name in ("info.json", *COVER_NAMES)):
            path.unlink()
    # A multi-part BV directory may still contain other selected tracks.
    while directory != BILIBILI_MUSIC and not any(directory.iterdir()):
        directory.rmdir()
        directory = directory.parent


def sync_bilibili(args: argparse.Namespace) -> None:
    cookie = load_cookie(args)
    medias = fetch_bilibili_favorite(resolve_media_id(args), cookie)
    tracks = read_track_plan(medias[:args.limit], cookie)
    expected = {t.directory for t in tracks}
    obsolete = stale_tracks(expected) if args.limit is None else []

    for track in tracks:
        action = "Download" if args.force or not has_audio(track.directory) else "Keep"
        print(f"{action}: {folder_key(track.directory)} — {track.info['name']}")
    for directory in obsolete:
        print(f"Remove: {folder_key(directory)}")
    if args.dry_run:
        return

    # Prepare downloads and metadata first. A failed request leaves the previous
    # playable files and playlist intact, including during a forced refresh.
    with tempfile.TemporaryDirectory(dir=ROOT, prefix=".music-stage-") as temp:
        stage = Path(temp)
        for track in tracks:
            pending = stage / folder_key(track.directory)
            pending.mkdir(parents=True)
            if args.force or not has_audio(track.directory):
                download_audio(track, pending, args.yt_dlp)
            if track.cover_url and (args.force or not (track.directory / "cover.jpg").is_file()):
                download_file(track.cover_url, pending / "cover.jpg")
            if load_json(track.directory / "info.json", {}) != track.info:
                write_json(pending / "info.json", track.info)

        for track in tracks:
            pending = stage / folder_key(track.directory)
            track.directory.mkdir(parents=True, exist_ok=True)
            for path in pending.iterdir():
                if path.name in ("info.json", "cover.jpg") or path.suffix.lower() in AUDIO_EXTS:
                    path.replace(track.directory / path.name)

    # Publish a complete index before retiring files that it no longer references.
    write_playlist(set(obsolete))
    for directory in sorted(obsolete, reverse=True):
        remove_stale(directory)


def require_music_files() -> None:
    # This blog is also edited in a sparse checkout; rebuilding from an incomplete
    # music directory would turn omitted files into real playlist removals.
    if not shutil.which("git"):
        return
    result = subprocess.run(["git", "ls-files", "-t", "-z", "--", "static/music", "data/music"],
                            cwd=ROOT, capture_output=True)
    for row in result.stdout.split(b"\0"):
        if row.startswith(b"S ") and not (ROOT / os.fsdecode(row[2:])).exists():
            raise RuntimeError("Materialize static/music and data/music in the sparse checkout before syncing.")


@contextmanager
def music_write_lock():
    lock = ROOT / ".music-sync.lock"
    try:
        lock.mkdir()
    except FileExistsError:
        raise RuntimeError(f"Another sync holds {lock}. If it was interrupted, remove the empty lock directory.")
    try:
        yield
    finally:
        lock.rmdir()


def positive_limit(value: str) -> int:
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError("limit must be at least 1")
    return n


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync the site music playlist.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("local", help="scan static/music and rebuild the local playlist")
    for name in ("bilibili", "all"):
        cmd = subparsers.add_parser(name, help="sync a Bilibili favorite list, then rebuild the playlist")
        cmd.add_argument("--media-id", help="Bilibili favorite media_id")
        cmd.add_argument("--favlist-url", help="Bilibili favorite list URL containing fid")
        cmd.add_argument("--cookie", help="raw Bilibili Cookie header")
        cmd.add_argument("--cookie-file", help="file containing raw Bilibili Cookie header")
        cmd.add_argument("--yt-dlp", default="yt-dlp", help="yt-dlp executable")
        cmd.add_argument("--force", action="store_true", help="redownload existing audio and cover")
        cmd.add_argument("--dry-run", action="store_true", help="show changes without writing files")
        cmd.add_argument("--limit", type=positive_limit, help="sync only the first N videos and skip all removals")

    return parser.parse_args()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    args = parse_args()
    try:
        if getattr(args, "dry_run", False):
            sync_bilibili(args)
        else:
            with music_write_lock():
                require_music_files()
                if args.command == "local":
                    write_playlist()
                else:
                    sync_bilibili(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
