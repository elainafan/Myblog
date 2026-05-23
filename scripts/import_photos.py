#!/usr/bin/env python3
"""Import curated local gallery images from public SFW anime image APIs."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import deque
from dataclasses import dataclass
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required: python -m pip install pillow") from exc


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "assets" / "waifus"
USER_AGENT = "ElainafanBlogPhotoImporter/1.0"


@dataclass(frozen=True)
class Candidate:
    url: str
    source: str


@dataclass
class ImportStats:
    accepted: int = 0
    rejected: int = 0
    failed: int = 0
    duplicate: int = 0


def request_json(url: str, params: dict[str, object] | None = None) -> dict:
    if params:
        url = f"{url}?{urllib.parse.urlencode(params, doseq=True)}"

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def request_json_list(url: str, params: dict[str, object] | None = None) -> list[dict]:
    if params:
        url = f"{url}?{urllib.parse.urlencode(params, doseq=True)}"

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def read_limited(url: str, max_bytes: int) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as resp:
        content_type = resp.headers.get("Content-Type", "")
        data = resp.read(max_bytes + 1)
    return data, content_type


def fetch_from_waifu_im() -> list[Candidate]:
    tags = ["waifu", "maid", "uniform", "selfies"]
    tag = random.choice(tags)
    data = request_json(
        "https://api.waifu.im/search",
        {
            "included_tags": [tag],
            "is_nsfw": "false",
            "gif": "false",
            "many": "true",
        },
    )
    return [
        Candidate(str(item["url"]), f"waifu.im:{tag}")
        for item in data.get("images", [])
        if item.get("url")
    ]


def fetch_from_nekos_best() -> list[Candidate]:
    endpoint = "waifu"
    data = request_json(f"https://nekos.best/api/v2/{endpoint}", {"amount": 20})
    return [
        Candidate(str(item["url"]), f"nekos.best:{endpoint}")
        for item in data.get("results", [])
        if item.get("url")
    ]


def fetch_from_waifu_pics() -> list[Candidate]:
    endpoint = random.choice(["waifu", "shinobu", "megumin"])
    data = request_json(f"https://api.waifu.pics/sfw/{endpoint}")
    url = data.get("url")
    return [Candidate(str(url), f"waifu.pics:{endpoint}")] if url else []


FAVORITE_DANBOORU_TAGS = [
    "k-on!",
    "akiyama_mio",
    "hirasawa_yui",
    "mahou_shoujo_madoka_magica",
    "akemi_homura",
    "kaname_madoka",
    "majo_no_tabitabi",
    "elaina_(majo_no_tabitabi)",
    "steins;gate",
    "makise_kurisu",
    "saenai_heroine_no_sodatekata",
    "sawamura_spencer_eriri",
    "new_game!",
    "suzumiya_haruhi_no_yuuutsu",
    "toradora!",
    "chuuni_byou_demo_koi_ga_shitai!",
    "hyouka",
    "yahari_ore_no_seishun_lovecome_wa_machigatteiru.",
    "yagate_kimi_ni_naru",
    "bocchi_the_rock!",
]

NEGATIVE_DANBOORU_TAGS = [
    "-rating:questionable",
    "-rating:explicit",
    "-animal_ears",
    "-cat_ears",
    "-dog_ears",
    "-fox_ears",
    "-bunny_ears",
    "-wolf_ears",
    "-tail",
    "-furry",
    "-comic",
    "-translated",
]

FAVORITE_SAFEBOORU_TAGS = [
    "k-on",
    "hirasawa_yui",
    "akiyama_mio",
    "nakano_azusa",
    "mahou_shoujo_madoka_magica",
    "kaname_madoka",
    "akemi_homura",
    "majo_no_tabitabi",
    "elaina_(majo_no_tabitabi)",
    "steins;gate",
    "makise_kurisu",
    "saenai_heroine_no_sodatekata",
    "sawamura_spencer_eriri",
    "new_game!",
    "suzumiya_haruhi_no_yuuutsu",
    "suzumiya_haruhi",
    "toradora!",
    "aisaka_taiga",
    "chuunibyou_demo_koi_ga_shitai!",
    "takanashi_rikka",
    "hyouka",
    "chitanda_eru",
    "yahari_ore_no_seishun_lovecome_wa_machigatteiru.",
    "yukinoshita_yukino",
    "yagate_kimi_ni_naru",
    "koito_yuu",
    "bocchi_the_rock!",
    "gotou_hitori",
]

GENERIC_SAFEBOORU_TAGS = [
    "1girl solo",
    "1girl school_uniform",
    "1girl seifuku",
    "1girl long_hair",
    "1girl short_hair",
    "1girl black_hair",
    "1girl brown_hair",
    "1girl blonde_hair",
    "1girl smile",
    "1girl dress",
    "1girl sitting",
    "1girl outdoors",
    "1girl sky",
    "1girl city",
    "1girl book",
    "1girl headphones",
    "1girl guitar",
    "1girl night",
]

NEGATIVE_SAFEBOORU_TAGS = [
    "-animal_ears",
    "-cat_ears",
    "-dog_ears",
    "-fox_ears",
    "-bunny_ears",
    "-wolf_ears",
    "-tail",
    "-furry",
    "-comic",
    "-manga",
    "-translated",
]


def fetch_from_danbooru() -> list[Candidate]:
    tag = random.choice(FAVORITE_DANBOORU_TAGS)
    tags = " ".join([tag, "rating:safe", "score:>=5", *NEGATIVE_DANBOORU_TAGS])
    posts = request_json_list(
        "https://danbooru.donmai.us/posts.json",
        {
            "tags": tags,
            "limit": 20,
            "random": "true",
        },
    )
    candidates: list[Candidate] = []
    for post in posts:
        url = post.get("file_url") or post.get("large_file_url")
        if url:
            candidates.append(Candidate(str(url), f"danbooru:{tag}"))
    return candidates


def fetch_from_safebooru(tag: str | None = None, pid: int | None = None) -> list[Candidate]:
    tag = tag or random.choice(FAVORITE_SAFEBOORU_TAGS)
    tags = " ".join([tag, "rating:safe", *NEGATIVE_SAFEBOORU_TAGS])
    posts = request_json_list(
        "https://safebooru.org/index.php",
        {
            "page": "dapi",
            "s": "post",
            "q": "index",
            "json": "1",
            "tags": tags,
            "limit": 40,
            "pid": pid if pid is not None else random.randint(0, 20),
        },
    )
    candidates: list[Candidate] = []
    random.shuffle(posts)
    for post in posts:
        url = post.get("sample_url") or post.get("file_url")
        if url:
            candidates.append(Candidate(str(url), f"safebooru:{tag}"))
    return candidates


def image_extension(image_format: str) -> str:
    normalized = image_format.lower()
    if normalized == "jpeg":
        return "jpg"
    return normalized


def inspect_image(data: bytes) -> tuple[str, int, int]:
    with Image.open(io.BytesIO(data)) as img:
        image_format = img.format or ""
        width, height = img.size
    return image_format, width, height


def normalize_image(data: bytes, quality: int) -> tuple[bytes, int, int]:
    with Image.open(io.BytesIO(data)) as img:
        img.load()
        width, height = img.size
        if img.mode in {"RGBA", "LA", "P"}:
            canvas = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            canvas.paste(img, mask=img.getchannel("A") if "A" in img.getbands() else None)
            img = canvas
        else:
            img = img.convert("RGB")

        output = io.BytesIO()
        img.save(output, format="WEBP", quality=quality, method=6)
    return output.getvalue(), width, height


def passes_quality(
    byte_size: int,
    image_format: str,
    width: int,
    height: int,
    args: argparse.Namespace,
) -> bool:
    if image_format.upper() not in {"JPEG", "PNG", "WEBP"}:
        return False
    if byte_size > args.max_bytes:
        return False
    if width * height < args.min_pixels:
        return False
    if max(width, height) < args.min_long_edge:
        return False
    if min(width, height) < args.min_short_edge:
        return False
    ratio = width / height
    if ratio < args.min_ratio or ratio > args.max_ratio:
        return False
    return True


def clear_output(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    root = ROOT.resolve()
    resolved = output.resolve()
    if not str(resolved).startswith(str(root)):
        raise SystemExit(f"Refusing to clear outside repository: {resolved}")

    for path in output.iterdir():
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
            path.unlink()


def existing_hashes(output: Path) -> set[str]:
    hashes: set[str] = set()
    for path in output.glob("*"):
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
            hashes.add(hashlib.sha256(path.read_bytes()).hexdigest())
    return hashes


def import_photos(args: argparse.Namespace) -> ImportStats:
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    if args.clear:
        clear_output(output)

    stats = ImportStats()
    seen_urls: set[str] = set()
    seen_hashes = existing_hashes(output)
    start_index = len(
        [
            path
            for path in output.glob("*")
            if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
        ]
    )
    attempts = 0
    max_attempts = max(args.count * args.attempt_factor, args.count)
    source_tags = GENERIC_SAFEBOORU_TAGS if args.source_set == "generic" else FAVORITE_SAFEBOORU_TAGS
    tag_queue = deque(source_tags)
    random.shuffle(tag_queue)
    tag_accepts = {tag: 0 for tag in source_tags}
    tag_pages = {tag: 0 for tag in source_tags}
    per_tag_target = max(1, (args.count + len(source_tags) - 1) // len(source_tags))
    batch_limit = max(1, args.per_tag_batch)

    while stats.accepted < args.count and attempts < max_attempts:
        attempts += 1
        if not tag_queue:
            tags = source_tags[:]
            random.shuffle(tags)
            tag_queue.extend(tags)
        tag = tag_queue.popleft()
        if tag_accepts[tag] >= per_tag_target and any(value < per_tag_target for value in tag_accepts.values()):
            continue

        try:
            candidates = fetch_from_safebooru(tag=tag, pid=tag_pages[tag])
            tag_pages[tag] += 1
        except Exception as exc:
            stats.failed += 1
            print(f"[api failed] safebooru:{tag}: {exc}", flush=True)
            time.sleep(args.delay)
            continue

        accepted_this_tag = 0
        for candidate in candidates:
            if stats.accepted >= args.count:
                break
            if accepted_this_tag >= batch_limit:
                break
            if candidate.url in seen_urls:
                continue
            seen_urls.add(candidate.url)

            try:
                data, content_type = read_limited(candidate.url, args.max_bytes)
                if len(data) > args.max_bytes:
                    stats.rejected += 1
                    print(f"[skip large] {candidate.url}", flush=True)
                    continue
                if "image" not in content_type.lower() and not candidate.url.lower().split("?")[0].endswith(
                    (".jpg", ".jpeg", ".png", ".webp")
                ):
                    stats.rejected += 1
                    print(f"[skip type] {candidate.url}", flush=True)
                    continue

                image_format, width, height = inspect_image(data)
                if not passes_quality(len(data), image_format, width, height, args):
                    stats.rejected += 1
                    print(f"[skip quality] {width}x{height} {image_format} {candidate.url}", flush=True)
                    continue

                normalized, width, height = normalize_image(data, args.quality)
                digest = hashlib.sha256(normalized).hexdigest()
                if digest in seen_hashes:
                    stats.duplicate += 1
                    print(f"[skip dup] {candidate.url}", flush=True)
                    continue

                ext = "webp"
                filename = f"{start_index + stats.accepted + 1:03d}-{digest[:12]}.{ext}"
                (output / filename).write_bytes(normalized)
                seen_hashes.add(digest)
                stats.accepted += 1
                tag_accepts[tag] += 1
                accepted_this_tag += 1
                print(f"[ok] {filename} {width}x{height} {candidate.source}", flush=True)
            except (urllib.error.URLError, OSError, ValueError) as exc:
                stats.failed += 1
                print(f"[download failed] {candidate.url}: {exc}", flush=True)

            time.sleep(args.delay)

        if tag_accepts[tag] < per_tag_target or not any(value < per_tag_target for value in tag_accepts.values()):
            tag_queue.append(tag)

    return stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=36, help="number of accepted images to keep")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="gallery output directory")
    parser.add_argument("--clear", action="store_true", help="remove existing gallery images first")
    parser.add_argument("--min-pixels", type=int, default=700_000)
    parser.add_argument("--min-long-edge", type=int, default=1000)
    parser.add_argument("--min-short-edge", type=int, default=520)
    parser.add_argument("--min-ratio", type=float, default=0.42)
    parser.add_argument("--max-ratio", type=float, default=2.5)
    parser.add_argument("--max-bytes", type=int, default=8 * 1024 * 1024)
    parser.add_argument("--quality", type=int, default=88, help="WebP output quality")
    parser.add_argument("--attempt-factor", type=int, default=10)
    parser.add_argument("--per-tag-batch", type=int, default=2, help="accepted images per tag per fetch")
    parser.add_argument(
        "--source-set",
        choices=["ip", "generic"],
        default="ip",
        help="tag pool to use when pulling Safebooru candidates",
    )
    parser.add_argument("--delay", type=float, default=0.05)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    stats = import_photos(args)
    print(
        f"accepted={stats.accepted} rejected={stats.rejected} "
        f"duplicate={stats.duplicate} failed={stats.failed}"
    )
    return 0 if stats.accepted > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
