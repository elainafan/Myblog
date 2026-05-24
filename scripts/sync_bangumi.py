#!/usr/bin/env python3
"""Fetch Bangumi anime collections and write Hugo data/bangumi/anime.json."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_USER = "1020990"
DEFAULT_OUTPUT = Path("data/bangumi/anime.json")
API_ROOT = "https://api.bgm.tv/v0"


def fetch_json(url: str, timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "ElainafanBlogBangumiSync/1.0 (https://www.elainafan.one)",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = response.read().decode("utf-8")
    return json.loads(payload)


def normalize_item(item: dict[str, Any]) -> dict[str, Any]:
    subject = item.get("subject") or {}
    images = subject.get("images") or {}
    return {
        "updated_at": item.get("updated_at"),
        "comment": item.get("comment"),
        "tags": item.get("tags") or [],
        "subject_id": item.get("subject_id"),
        "subject_type": item.get("subject_type"),
        "type": item.get("type"),
        "rate": item.get("rate") or 0,
        "ep_status": item.get("ep_status") or 0,
        "vol_status": item.get("vol_status") or 0,
        "private": item.get("private") or False,
        "subject": {
            "id": subject.get("id"),
            "name": subject.get("name"),
            "name_cn": subject.get("name_cn"),
            "date": subject.get("date"),
            "score": subject.get("score"),
            "rank": subject.get("rank"),
            "eps": subject.get("eps") or 0,
            "collection_total": subject.get("collection_total"),
            "images": {
                "grid": images.get("grid"),
                "common": images.get("common"),
                "medium": images.get("medium"),
                "large": images.get("large"),
            },
        },
    }


def fetch_collections(user: str, subject_type: int, limit: int, timeout: int) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    offset = 0
    total = None

    while True:
        query = urllib.parse.urlencode(
            {
                "subject_type": subject_type,
                "limit": limit,
                "offset": offset,
            }
        )
        url = f"{API_ROOT}/users/{urllib.parse.quote(user)}/collections?{query}"
        data = fetch_json(url, timeout)

        page_items = data.get("data") or []
        items.extend(normalize_item(item) for item in page_items)
        total = data.get("total", len(items))

        offset += len(page_items)
        if not page_items or offset >= total:
            break

    return {
        "source": "bangumi",
        "user": user,
        "subject_type": subject_type,
        "total": total or len(items),
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", default=DEFAULT_USER, help="Bangumi username or numeric user id.")
    parser.add_argument("--subject-type", type=int, default=2, help="Bangumi subject type, 2 means anime.")
    parser.add_argument("--limit", type=int, default=100, help="Page size for API requests.")
    parser.add_argument("--timeout", type=int, default=15, help="HTTP timeout in seconds.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    try:
        data = fetch_collections(args.user, args.subject_type, args.limit, args.timeout)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"Failed to fetch Bangumi collections: {exc}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(data['data'])} Bangumi items to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
