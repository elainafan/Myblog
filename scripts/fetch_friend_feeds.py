#!/usr/bin/env python3
"""Fetch friend RSS/Atom feeds and write Hugo data/friend_posts.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path
from typing import Any
from xml.etree import ElementTree


DEFAULT_SETTINGS = {
    "max_posts": 80,
    "max_posts_per_friend": 6,
    "max_days": 180,
    "timeout": 15,
}


def strip_comment(line: str) -> str:
    in_single = False
    in_double = False
    for i, char in enumerate(line):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            return line[:i]
    return line


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "none", "~"}:
        return None
    try:
        return int(value)
    except ValueError:
        return value


def parse_simple_yaml(path: Path) -> dict[str, Any]:
    root: dict[str, Any] = {}
    current_section: str | None = None
    current_item: dict[str, Any] | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        cleaned = strip_comment(raw_line).rstrip()
        if not cleaned.strip():
            continue
        indent = len(cleaned) - len(cleaned.lstrip(" "))
        line = cleaned.strip()

        if indent == 0 and line.endswith(":"):
            current_section = line[:-1].strip()
            root[current_section] = [] if current_section == "friends" else {}
            current_item = None
            continue

        if indent == 0 and ":" in line:
            key, value = line.split(":", 1)
            root[key.strip()] = parse_scalar(value)
            current_section = None
            current_item = None
            continue

        if current_section == "friends":
            friends = root.setdefault("friends", [])
            if line.startswith("- "):
                current_item = {}
                friends.append(current_item)
                rest = line[2:].strip()
                if rest and ":" in rest:
                    key, value = rest.split(":", 1)
                    current_item[key.strip()] = parse_scalar(value)
                continue
            if current_item is not None and ":" in line:
                key, value = line.split(":", 1)
                current_item[key.strip()] = parse_scalar(value)
            continue

        if current_section and isinstance(root.get(current_section), dict) and ":" in line:
            key, value = line.split(":", 1)
            root[current_section][key.strip()] = parse_scalar(value)

    return root


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def first_child_text(element: ElementTree.Element, names: set[str]) -> str:
    for child in list(element):
        if local_name(child.tag) in names:
            return "".join(child.itertext()).strip()
    return ""


def entry_link(entry: ElementTree.Element) -> str:
    for child in list(entry):
        if local_name(child.tag) != "link":
            continue
        href = child.attrib.get("href", "").strip()
        rel = child.attrib.get("rel", "alternate")
        if href and rel == "alternate":
            return href
        text = "".join(child.itertext()).strip()
        if text:
            return text
    return ""


def parse_date(value: str) -> datetime | None:
    if not value:
        return None
    value = value.strip()
    try:
        dt = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def clean_summary(value: str, limit: int = 180) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    text = unescape(re.sub(r"\s+", " ", text)).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "..."


def fetch_text(url: str, timeout: int) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "hugo-friend-circle/0.1 (+https://github.com/elainafan/hugo-friend-circle)"
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def parse_feed(feed_xml: bytes, friend: dict[str, Any]) -> list[dict[str, Any]]:
    root = ElementTree.fromstring(feed_xml)
    entries = [
        element
        for element in root.iter()
        if local_name(element.tag) in {"item", "entry"}
    ]
    posts: list[dict[str, Any]] = []
    for entry in entries:
        published_raw = first_child_text(
            entry, {"pubDate", "published", "updated", "date", "created"}
        )
        published = parse_date(published_raw)
        summary = first_child_text(entry, {"description", "summary", "content", "encoded"})
        url = entry_link(entry) or first_child_text(entry, {"guid", "id"})
        title = first_child_text(entry, {"title"}) or "Untitled"
        posts.append(
            {
                "friend": friend.get("name", ""),
                "site": friend.get("site", ""),
                "feed": friend.get("feed", ""),
                "avatar": friend.get("avatar", ""),
                "title": title,
                "url": url,
                "summary": clean_summary(summary),
                "published": published.isoformat() if published else "",
                "published_text": published_raw,
            }
        )
    return posts


def normalize_friend(friend: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": str(friend.get("name", "")).strip(),
        "site": str(friend.get("site", "")).strip(),
        "feed": str(friend.get("feed", "")).strip(),
        "avatar": str(friend.get("avatar", "")).strip(),
        "description": str(friend.get("description", "")).strip(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--friends", default="data/friends.yaml")
    parser.add_argument("--output", default="data/friend_posts.json")
    args = parser.parse_args()

    friends_path = Path(args.friends)
    output_path = Path(args.output)
    raw_config = parse_simple_yaml(friends_path)
    settings = DEFAULT_SETTINGS | dict(raw_config.get("settings") or {})
    friends = [normalize_friend(friend) for friend in raw_config.get("friends", [])]

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=int(settings["max_days"]))
    timeout = int(settings["timeout"])
    all_posts: list[dict[str, Any]] = []
    warnings: list[dict[str, str]] = []
    friend_status: dict[str, dict[str, Any]] = {}

    for friend in friends:
        name = friend["name"] or friend["feed"]
        friend_status[name] = {**friend, "status": "ok", "post_count": 0}
        if not friend["feed"]:
            friend_status[name]["status"] = "warning"
            warnings.append({"friend": name, "message": "missing feed URL"})
            continue
        try:
            feed_xml = fetch_text(friend["feed"], timeout)
            posts = parse_feed(feed_xml, friend)
        except (urllib.error.URLError, TimeoutError, ElementTree.ParseError, ValueError) as exc:
            friend_status[name]["status"] = "warning"
            warnings.append({"friend": name, "message": str(exc)})
            continue

        filtered: list[dict[str, Any]] = []
        for post in posts:
            published = parse_date(post["published"])
            if published and published < cutoff:
                continue
            filtered.append(post)
        filtered.sort(key=lambda post: post.get("published") or "", reverse=True)
        limited = filtered[: int(settings["max_posts_per_friend"])]
        friend_status[name]["post_count"] = len(limited)
        all_posts.extend(limited)

    seen_urls: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for post in sorted(all_posts, key=lambda item: item.get("published") or "", reverse=True):
        key = post.get("url") or f"{post.get('friend')}:{post.get('title')}"
        if key in seen_urls:
            continue
        seen_urls.add(key)
        deduped.append(post)

    payload = {
        "generated_at": now.isoformat(),
        "settings": settings,
        "friends": list(friend_status.values()),
        "warnings": warnings,
        "posts": deduped[: int(settings["max_posts"])],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {output_path} with {len(payload['posts'])} posts")
    if warnings:
        print(f"{len(warnings)} warning(s); build can continue", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
