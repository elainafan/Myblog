#!/usr/bin/env python3
"""
Build the APlayer playlist from local music folders and, optionally, a Bilibili
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
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATIC_MUSIC = ROOT / "static" / "music"
LOCAL_META = ROOT / "data" / "music" / "local.json"
GENERATED_PLAYLIST = ROOT / "data" / "music" / "generated.json"
SOURCES_CONFIG = ROOT / "data" / "music" / "sources.json"
BILIBILI_MUSIC = STATIC_MUSIC / "bilibili"

AUDIO_NAMES = ("music.mp3", "music.m4a", "music.ogg", "music.flac", "music.wav")
AUDIO_EXTS = (".mp3", ".m4a", ".ogg", ".flac", ".wav")
COVER_NAMES = ("cover.jpg", "cover.jpeg", "cover.png", "cover.webp", "music.jpg", "music.png")


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


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


def build_playlist() -> list[dict[str, Any]]:
    local_entries = load_json(LOCAL_META, [])
    overrides = load_music_overrides()

    seen_dirs: set[Path] = set()
    tracks: list[dict[str, Any]] = []

    for entry in local_entries:
        folder = entry.get("folder") if isinstance(entry, dict) else None
        if not folder:
            continue
        directory = STATIC_MUSIC / folder
        track = discover_track(directory, overrides) if directory.exists() else None
        if track:
            tracks.append(track)
            seen_dirs.add(directory.resolve())

    for directory in sorted(path for path in STATIC_MUSIC.rglob("*") if path.is_dir()):
        if directory.resolve() in seen_dirs:
            continue
        track = discover_track(directory, overrides)
        if track:
            tracks.append(track)

    return tracks


def write_playlist() -> None:
    playlist = build_playlist()
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
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.bilibili.com/",
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
    while True:
        query = urllib.parse.urlencode({"media_id": media_id, "pn": page, "ps": 20})
        payload = http_get_json(f"https://api.bilibili.com/x/v3/fav/resource/list?{query}", cookie)
        if payload.get("code") != 0:
            raise RuntimeError(f"Bilibili API error: {payload.get('message') or payload}")

        data = payload.get("data") or {}
        batch = data.get("medias") or []
        medias.extend(batch)

        if not data.get("has_more") or not batch:
            break
        page += 1
        time.sleep(0.4)

    return medias


def safe_name(value: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value)
    return value.strip(" .") or "unknown"


def download_cover(url: str, target: Path, force: bool) -> None:
    if target.exists() and not force:
        return
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        target.write_bytes(response.read())


def has_audio(directory: Path) -> bool:
    return find_audio(directory) is not None


def sync_bilibili(args: argparse.Namespace) -> None:
    cookie = load_cookie(args)
    media_id = resolve_media_id(args)
    overrides = load_music_overrides()
    medias = fetch_bilibili_favorite(media_id, cookie)
    if args.limit:
        medias = medias[: args.limit]
    if not args.dry_run:
        BILIBILI_MUSIC.mkdir(parents=True, exist_ok=True)

    for media in medias:
        bvid = media.get("bvid")
        if not bvid:
            continue

        title = media.get("title") or bvid
        artist = (media.get("upper") or {}).get("name") or "Bilibili"
        page_url = f"https://www.bilibili.com/video/{bvid}"
        directory = BILIBILI_MUSIC / safe_name(bvid)

        if args.dry_run:
            command = [
                args.yt_dlp,
                "-f",
                "bestaudio/best",
                "--no-playlist",
            ]
            command.extend(["-o", str(directory / "music.%(ext)s"), page_url])
            print(f"Download audio: {bvid} {title}")
            print(" ".join(command))
            continue

        directory.mkdir(parents=True, exist_ok=True)

        info = {
            "name": title,
            "artist": artist,
            "source": "bilibili",
            "bvid": bvid,
            "sourceUrl": page_url,
        }
        override = overrides.get(folder_key(directory), overrides.get(directory.name, {}))
        for key in ("name", "artist"):
            if override.get(key):
                info[key] = override[key]
        write_json(directory / "info.json", info)

        cover_url = media.get("cover")
        if cover_url:
            download_cover(cover_url, directory / "cover.jpg", args.force)

        if has_audio(directory) and not args.force:
            print(f"Skip existing audio: {bvid} {title}")
            continue

        command = [
            args.yt_dlp,
            "-f",
            "bestaudio/best",
            "--no-playlist",
        ]
        command.extend(["-o", str(directory / "music.%(ext)s"), page_url])
        print(f"Download audio: {bvid} {title}")
        subprocess.run(command, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync APlayer music playlist.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("local", help="scan static/music and rebuild data/music/generated.json")

    bilibili = subparsers.add_parser("bilibili", help="sync a Bilibili favorite list, then rebuild playlist")
    bilibili.add_argument("--media-id", help="Bilibili favorite media_id")
    bilibili.add_argument("--favlist-url", help="Bilibili favorite list URL containing fid")
    bilibili.add_argument("--cookie", help="raw Bilibili Cookie header")
    bilibili.add_argument("--cookie-file", help="file containing raw Bilibili Cookie header")
    bilibili.add_argument("--yt-dlp", default="yt-dlp", help="yt-dlp executable")
    bilibili.add_argument("--force", action="store_true", help="redownload existing audio and cover")
    bilibili.add_argument("--dry-run", action="store_true", help="print yt-dlp commands without downloading audio")
    bilibili.add_argument("--limit", type=int, help="sync only the first N videos")

    all_cmd = subparsers.add_parser("all", help="sync Bilibili favorite list and local folders")
    all_cmd.add_argument("--media-id", help="Bilibili favorite media_id")
    all_cmd.add_argument("--favlist-url", help="Bilibili favorite list URL containing fid")
    all_cmd.add_argument("--cookie", help="raw Bilibili Cookie header")
    all_cmd.add_argument("--cookie-file", help="file containing raw Bilibili Cookie header")
    all_cmd.add_argument("--yt-dlp", default="yt-dlp", help="yt-dlp executable")
    all_cmd.add_argument("--force", action="store_true", help="redownload existing audio and cover")
    all_cmd.add_argument("--dry-run", action="store_true", help="print yt-dlp commands without downloading audio")
    all_cmd.add_argument("--limit", type=int, help="sync only the first N videos")

    return parser.parse_args()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    args = parse_args()
    try:
        if args.command in {"bilibili", "all"}:
            sync_bilibili(args)
        write_playlist()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
