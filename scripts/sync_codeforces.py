#!/usr/bin/env python3
"""Sync rated Codeforces round stats after a given round.

The script intentionally updates only rated contests that appear in
Codeforces rating history for the configured handles. VP / unrated / manual
upsolve records are left alone.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


BLOG_ROOT = Path(__file__).resolve().parents[1]
CODEFORCES_DATA = BLOG_ROOT / "data" / "codeforces.yaml"
CODEFORCES_MAIN = BLOG_ROOT / "content" / "post" / "\u4e8c\u6b21\u5143\u4fee\u70bc\u65e5\u8bb0\uff01" / "main.md"
DEFAULT_HANDLES = ("PaperMemory", "Kuro_neko")
TASK_COLUMNS = list("ABCDEFGHI")
CHECK = "\u221a"
MANUAL_MARKERS = {"B", "H", "N"}


@dataclass
class ContestUpdate:
    handle: str
    rank: str
    perf: str
    solved: int
    accepted_columns: set[str]


def request_json(method: str, **params: Any) -> Any:
    url = f"https://codeforces.com/api/{method}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (hugo codeforces sync; +https://www.elainafan.one/)",
        },
    )
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
            if payload.get("status") != "OK":
                raise RuntimeError(payload.get("comment") or payload)
            return payload["result"]
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt < 3:
                time.sleep(1.2 * (attempt + 1))
    raise RuntimeError(f"Codeforces API request failed: {method}: {last_error}")


def parse_simple_yaml(path: Path) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("  - "):
            if current:
                records.append(current)
            current = {}
            key, value = line[4:].split(":", 1)
            current[key] = unquote_yaml(value)
        elif current is not None and line.startswith("    ") and ":" in line:
            key, value = line.strip().split(":", 1)
            current[key] = unquote_yaml(value)
    if current:
        records.append(current)
    return records


def unquote_yaml(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return json.loads(value)
    return value


def yaml_string(value: Any) -> str:
    return json.dumps("" if value is None else str(value), ensure_ascii=False)


def write_codeforces_yaml(path: Path, records: list[dict[str, str]]) -> None:
    lines = ["contests:"]
    field_order = ["date", "round", "div", "group", "contest", "solved", "rank", "perf", "ref"]
    for record in records:
        lines.append(f"  - date: {yaml_string(record.get('date', ''))}")
        for field in field_order[1:]:
            if field not in record:
                continue
            value = record[field]
            if field == "solved" and str(value).isdigit():
                lines.append(f"    {field}: {value}")
            else:
                lines.append(f"    {field}: {yaml_string(value)}")
        for field, value in record.items():
            if field not in field_order:
                lines.append(f"    {field}: {yaml_string(value)}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def fetch_rating_history(handles: tuple[str, ...]) -> dict[str, tuple[str, dict[str, Any]]]:
    by_contest: dict[str, tuple[str, dict[str, Any]]] = {}
    for handle in handles:
        history = request_json("user.rating", handle=handle)
        for item in history:
            contest_id = str(item["contestId"])
            by_contest.setdefault(contest_id, (handle, item))
        time.sleep(0.35)
    return by_contest


def fetch_submissions(handles: tuple[str, ...]) -> dict[str, list[dict[str, Any]]]:
    all_submissions: dict[str, list[dict[str, Any]]] = {}
    for handle in handles:
        submissions: list[dict[str, Any]] = []
        start = 1
        page_size = 10000
        while True:
            page = request_json("user.status", handle=handle, **{"from": start, "count": page_size})
            submissions.extend(page)
            if len(page) < page_size:
                break
            start += page_size
            time.sleep(0.35)
        all_submissions[handle] = submissions
        time.sleep(0.35)
    return all_submissions


def accepted_for_contest(submissions: list[dict[str, Any]], contest_id: str) -> set[str]:
    accepted: set[str] = set()
    numeric_id = int(contest_id)
    for submission in submissions:
        if submission.get("contestId") != numeric_id:
            continue
        author = submission.get("author", {})
        if author.get("participantType") != "CONTESTANT":
            continue
        if submission.get("verdict") != "OK":
            continue
        index = str(submission.get("problem", {}).get("index", ""))
        if index:
            accepted.add(index)
    return accepted


def problem_sort_key(index: str) -> tuple[str, int]:
    match = re.fullmatch(r"([A-Z]+)(\d*)", index)
    if not match:
        return (index, 0)
    head, tail = match.groups()
    return (head, int(tail or 0))


def accepted_columns(accepted_indexes: set[str], problem_columns: dict[str, str]) -> set[str]:
    columns: set[str] = set()
    if problem_columns:
        for index in accepted_indexes:
            column = problem_columns.get(index)
            if column:
                columns.add(column)
        return columns

    has_split_problem = any(re.search(r"\d", index) for index in accepted_indexes)
    if has_split_problem:
        for position, index in enumerate(sorted(accepted_indexes, key=problem_sort_key)):
            if position < len(TASK_COLUMNS):
                columns.add(TASK_COLUMNS[position])
        return columns

    for index in accepted_indexes:
        match = re.match(r"([A-Z])", index)
        if match and match.group(1) in TASK_COLUMNS:
            columns.add(match.group(1))
    return columns


def estimate_performance(contest_id: str, target_handle: str) -> str:
    changes = request_json("contest.ratingChanges", contestId=contest_id)
    target = next((item for item in changes if item["handle"].lower() == target_handle.lower()), None)
    if target is None:
        return ""

    rank = int(target["rank"])
    target_lower = target["handle"].lower()
    ratings = [
        int(item["oldRating"])
        for item in changes
        if item["handle"].lower() != target_lower and int(item.get("oldRating") or 0) > 0
    ]
    if not ratings:
        return ""

    def expected_rank(rating: float) -> float:
        return 1.0 + sum(1.0 / (1.0 + math.pow(10.0, (rating - other) / 400.0)) for other in ratings)

    low, high = 1.0, 4000.0
    for _ in range(60):
        mid = (low + high) / 2.0
        if expected_rank(mid) > rank:
            low = mid
        else:
            high = mid
    return str(round((low + high) / 2.0))


def parse_existing_table(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    table: dict[str, dict[str, str]] = {}
    for line in text.splitlines():
        if not line.startswith("| 20"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 16:
            continue
        contest_match = re.search(r"\[(\d+)\]", cells[3])
        if not contest_match:
            continue
        status = {column: cells[7 + index] if 7 + index < len(cells) else "" for index, column in enumerate(TASK_COLUMNS)}
        table[contest_match.group(1)] = status
    return table


def merge_status(old_status: dict[str, str], official_columns: set[str]) -> dict[str, str]:
    merged: dict[str, str] = {}
    for column in TASK_COLUMNS:
        old = old_status.get(column, "").strip()
        if column in official_columns:
            merged[column] = CHECK
        elif old == CHECK:
            merged[column] = "B"
        elif old in MANUAL_MARKERS:
            merged[column] = old
        else:
            merged[column] = old if old not in {"-", " "} else ""
    return merged


def build_updates(
    records: list[dict[str, str]],
    handles: tuple[str, ...],
    since_round: str,
) -> tuple[dict[str, ContestUpdate], list[str]]:
    rating_history = fetch_rating_history(handles)
    submissions = fetch_submissions(handles)
    since_date = next(record["date"] for record in records if record.get("round") == since_round)

    updates: dict[str, ContestUpdate] = {}
    notes: list[str] = []
    for record in records:
        if record.get("date", "") < since_date:
            continue
        contest_id = record.get("contest", "")
        if contest_id not in rating_history:
            continue
        handle, rating = rating_history[contest_id]
        accepted = accepted_for_contest(submissions.get(handle, []), contest_id)
        perf = estimate_performance(contest_id, handle)
        time.sleep(0.35)
        update = ContestUpdate(
            handle=handle,
            rank=str(rating["rank"]),
            perf=perf or str(record.get("perf", "")),
            solved=len(accepted),
            accepted_columns=accepted_columns(accepted, {}),
        )
        changed = []
        if str(record.get("rank", "")) != update.rank:
            changed.append(f"rank {record.get('rank')}->{update.rank}")
        if str(record.get("perf", "")) != update.perf:
            changed.append(f"perf {record.get('perf')}->{update.perf}")
        if str(record.get("solved", "")) != str(update.solved):
            changed.append(f"solved {record.get('solved')}->{update.solved}")
        if changed:
            notes.append(f"{record.get('round')} ({contest_id}, {handle}): " + ", ".join(changed))
        updates[contest_id] = update
    return updates, notes


def apply_updates(
    records: list[dict[str, str]],
    updates: dict[str, ContestUpdate],
    old_statuses: dict[str, dict[str, str]],
) -> dict[str, dict[str, str]]:
    statuses: dict[str, dict[str, str]] = {}
    for record in records:
        contest_id = record.get("contest", "")
        old_status = old_statuses.get(contest_id, {})
        update = updates.get(contest_id)
        if update is None:
            statuses[contest_id] = {column: old_status.get(column, "") for column in TASK_COLUMNS}
            continue
        record["rank"] = update.rank
        record["perf"] = update.perf
        record["solved"] = str(update.solved)
        statuses[contest_id] = merge_status(old_status, update.accepted_columns)
    return statuses


def render_table(records: list[dict[str, str]], statuses: dict[str, dict[str, str]]) -> str:
    lines = [
        "| Date | Round | div | id | sol | rk | perf | " + " | ".join(TASK_COLUMNS) + " |",
        "| ---- | ----- | --- | -- | --- | -- | ---- | " + " | ".join("-" for _ in TASK_COLUMNS) + " |",
    ]
    for record in records:
        ref = '{{< ref "' + record.get("ref", "") + '" >}}'
        contest_id = record.get("contest", "")
        status = statuses.get(contest_id, {})
        cells = [status.get(column, "") for column in TASK_COLUMNS]
        lines.append(
            "| {date} | [{round}]({ref}) | {div} | [{contest}](https://codeforces.com/contest/{contest}) | "
            "{solved} | {rank} | {perf} | {tasks} |".format(
                date=record.get("date", "").replace("-", "."),
                round=record.get("round", ""),
                ref=ref,
                div=record.get("div", ""),
                contest=contest_id,
                solved=record.get("solved", ""),
                rank=record.get("rank", ""),
                perf=record.get("perf", ""),
                tasks=" | ".join(cells),
            )
        )
    return "\n".join(lines)


def replace_codeforces_table(path: Path, table: str) -> None:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(## \u770b\u756a\u65e5\u8bb0\n)(.*?)(\n## \u6bd4\u8d5b\u590d\u76d8)", text, flags=re.S)
    if not match:
        raise RuntimeError(f"Codeforces table block not found in {path}")
    new_text = text[: match.start(2)] + table + "\n" + text[match.start(3) :]
    path.write_text(new_text, encoding="utf-8")


def ensure_update_note(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    note = "      content: \u540c\u6b65 R1060 \u4e4b\u540e Rated rounds \u7684\u5b98\u65b9 rank\u3001Performance \u4e0e\u8d5b\u65f6\u8fc7\u9898\u72b6\u6001\u3002"
    if note in text:
        return
    marker = "updates:\n"
    if marker not in text:
        return
    insert = "    - date: 2026-05-28\n" + note + "\n"
    text = text.replace(marker, marker + insert, 1)
    path.write_text(text, encoding="utf-8")


def sync(handles: tuple[str, ...], since_round: str) -> list[str]:
    records = parse_simple_yaml(CODEFORCES_DATA)
    old_statuses = parse_existing_table(CODEFORCES_MAIN)
    updates, notes = build_updates(records, handles, since_round)
    statuses = apply_updates(records, updates, old_statuses)
    write_codeforces_yaml(CODEFORCES_DATA, records)
    replace_codeforces_table(CODEFORCES_MAIN, render_table(records, statuses))
    ensure_update_note(CODEFORCES_MAIN)
    return notes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--since-round", default="R1060")
    parser.add_argument("--handles", default=",".join(DEFAULT_HANDLES))
    args = parser.parse_args()

    handles = tuple(handle.strip() for handle in args.handles.split(",") if handle.strip())
    notes = sync(handles, args.since_round)
    if notes:
        print("\n".join(notes))
    else:
        print("No rated Codeforces changes needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
