#!/usr/bin/env python3
"""Sync the AtCoder diary from Shiro_neko's public history and local CP files."""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


BLOG_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CP_ROOT = BLOG_ROOT.parents[1] / "CP" / "Atcoder"
DEFAULT_HANDLE = "Shiro_neko"
SERIES_TITLE = "放学后喝茶日记！"
SERIES_DIR = BLOG_ROOT / "content" / "post" / SERIES_TITLE
DEFAULT_IMAGE = "/images/anime-diary/5.png"
CHECK = "√"
MISS_PERF_THRESHOLD = 100
HIGH_MISS_RANK = 8000

KIND_NAMES = {
    "ABC": "AtCoder Beginner Contest",
    "ARC": "AtCoder Regular Contest",
}


@dataclass
class Task:
    label: str
    problem_id: str
    url: str
    path: Path | None = None
    status: str = ""


@dataclass
class Contest:
    date: str
    round: str
    title: str
    div: str
    group: str
    contest: str
    url: str
    ref: str
    tasks: list[Task]
    solved: int = 0
    rank: str = "vp"
    perf: str = "vp"
    rating: str = ""
    missed: bool = False


def run_curl(url: str, accept: str = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8") -> str:
    command = [
        "curl.exe",
        "-L",
        "-sS",
        "-A",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
        "-H",
        f"Accept: {accept}",
        "-H",
        "Accept-Language: en-US,en;q=0.9",
        "-H",
        "Referer: https://atcoder.jp/",
        url,
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True, encoding="utf-8")
    return result.stdout


def fetch_history(handle: str) -> list[dict[str, Any]]:
    url = f"https://atcoder.jp/users/{handle}/history/json"
    payload = run_curl(url, "application/json,text/plain,*/*")
    return json.loads(payload)


def label_sort_key(label: str) -> tuple[str, int]:
    match = re.fullmatch(r"([A-Z]+)(\d*)", label.upper())
    if not match:
        return (label.upper(), 0)
    head, tail = match.groups()
    return (head, int(tail or 0))


def problem_label_from_path(path: Path, contest_id: str) -> str | None:
    stem = path.stem.lower()
    prefix = contest_id.lower()
    if stem.startswith(prefix):
        suffix = stem[len(prefix) :]
        if re.fullmatch(r"[a-z]\d*", suffix):
            return suffix.upper()
    match = re.search(r"([A-Za-z]\d*)$", path.stem)
    return match.group(1).upper() if match else None


def atcoder_problem_url(contest_id: str, label: str) -> str:
    return f"https://atcoder.jp/contests/{contest_id}/tasks/{contest_id}_{label.lower()}"


def title_for(kind: str, number: str, fallback: str = "") -> str:
    return f"{KIND_NAMES.get(kind, 'AtCoder Contest')} {number}" if number else fallback


def ref_for(kind: str, number: str, contest_id: str) -> str:
    return f"{kind.lower()}-{number}.md" if number else f"{contest_id}.md"


def parse_contest_id(screen_name: str) -> str:
    return screen_name.split(".", 1)[0].lower()


def round_from_contest_id(contest_id: str) -> tuple[str, str, str]:
    match = re.fullmatch(r"([a-z]+)(\d+)", contest_id.lower())
    if not match:
        return contest_id.upper(), contest_id.upper(), ""
    kind, number = match.groups()
    upper_kind = kind.upper()
    return upper_kind, f"{upper_kind}{number}", number


def discover_cp(cp_root: Path) -> dict[str, Contest]:
    contests: dict[str, Contest] = {}
    if not cp_root.exists():
        return contests

    for directory in sorted(path for path in cp_root.glob("*/*") if path.is_dir()):
        match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})\s+([A-Z]+)(\d+)", directory.name)
        if not match:
            continue
        date, kind, number = match.groups()
        contest_id = f"{kind.lower()}{number}"
        tasks_by_label: dict[str, Task] = {}
        for path in sorted(directory.glob("*.cpp"), key=lambda item: label_sort_key(problem_label_from_path(item, contest_id) or item.stem)):
            label = problem_label_from_path(path, contest_id)
            if not label:
                continue
            tasks_by_label[label] = Task(
                label=label,
                problem_id=f"{contest_id}_{label.lower()}",
                url=atcoder_problem_url(contest_id, label),
                path=path,
                status="B",
            )
        if kind == "ABC":
            for label in ("A", "B", "C"):
                tasks_by_label.setdefault(
                    label,
                    Task(
                        label=label,
                        problem_id=f"{contest_id}_{label.lower()}",
                        url=atcoder_problem_url(contest_id, label),
                        status=CHECK,
                    ),
                )
        if not tasks_by_label:
            continue
        tasks = sorted(tasks_by_label.values(), key=lambda task: label_sort_key(task.label))
        contests[contest_id] = Contest(
            date=date,
            round=f"{kind}{number}",
            title=title_for(kind, number),
            div=kind,
            group=kind.lower(),
            contest=contest_id,
            url=f"https://atcoder.jp/contests/{contest_id}",
            ref=ref_for(kind, number, contest_id),
            tasks=tasks,
            solved=sum(1 for task in tasks if task.status == CHECK or task.path is not None),
        )
    return contests


def fetch_task_labels(contest_id: str) -> list[str]:
    try:
        page = run_curl(f"https://atcoder.jp/contests/{contest_id}/tasks")
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] failed to fetch AtCoder tasks for {contest_id}: {exc}", file=sys.stderr)
        kind, _, _ = round_from_contest_id(contest_id)
        return list("ABCDEFG") if kind == "ABC" else list("ABCDEF")

    labels: set[str] = set()
    pattern = re.compile(rf'href="/contests/{re.escape(contest_id)}/tasks/{re.escape(contest_id)}_([a-z]\d*)"', re.I)
    for match in pattern.finditer(page):
        labels.add(match.group(1).upper())
    return sorted(labels, key=label_sort_key)


def parse_old_statuses(main_path: Path) -> tuple[dict[str, dict[str, str]], dict[str, int]]:
    if not main_path.exists():
        return {}, {}
    statuses: dict[str, dict[str, str]] = {}
    solved: dict[str, int] = {}
    for line in main_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.startswith("| 20"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 8:
            continue
        contest_match = re.search(r"contests/([a-z]+\d+)", cells[3], flags=re.I)
        if not contest_match:
            continue
        contest_id = contest_match.group(1).lower()
        if cells[4].isdigit():
            solved[contest_id] = int(cells[4])
        task_cells = cells[7:]
        statuses[contest_id] = {
            chr(ord("A") + index): value
            for index, value in enumerate(task_cells)
            if value
        }
    return statuses, solved


def is_missed(history_item: dict[str, Any]) -> bool:
    performance = int(history_item.get("Performance") or 0)
    place = int(history_item.get("Place") or 0)
    rated = bool(history_item.get("IsRated"))
    if rated and performance < MISS_PERF_THRESHOLD:
        return True
    return not rated and place >= HIGH_MISS_RANK


def merge_history(cp_contests: dict[str, Contest], history: list[dict[str, Any]], old_solved: dict[str, int]) -> dict[str, Contest]:
    contests = dict(cp_contests)
    for item in history:
        contest_id = parse_contest_id(str(item.get("ContestScreenName", "")))
        if not re.fullmatch(r"(abc|arc)\d+", contest_id):
            continue
        kind, round_name, number = round_from_contest_id(contest_id)
        date = str(item.get("EndTime", ""))[:10] or cp_contests.get(contest_id, Contest("", "", "", "", "", "", "", "", [])).date
        contest = contests.get(contest_id)
        if contest is None:
            labels = fetch_task_labels(contest_id)
            tasks = [
                Task(
                    label=label,
                    problem_id=f"{contest_id}_{label.lower()}",
                    url=atcoder_problem_url(contest_id, label),
                    status="",
                )
                for label in labels
            ]
            contest = Contest(
                date=date,
                round=round_name,
                title=title_for(kind, number, str(item.get("ContestNameEn") or item.get("ContestName") or round_name)),
                div=kind,
                group=kind.lower(),
                contest=contest_id,
                url=f"https://atcoder.jp/contests/{contest_id}",
                ref=ref_for(kind, number, contest_id),
                tasks=tasks,
            )
            contests[contest_id] = contest
        else:
            contest.date = contest.date or date

        missed = is_missed(item)
        contest.missed = missed
        contest.rating = str(item.get("NewRating", ""))
        if missed:
            contest.rank = "missed"
            contest.perf = "missed"
            contest.solved = 0
        elif item.get("IsRated"):
            contest.rank = str(item.get("Place", ""))
            contest.perf = str(item.get("Performance", ""))
        else:
            contest.rank = str(item.get("Place", "unrated"))
            contest.perf = "unrated"

        if not missed:
            if contest_id in old_solved:
                contest.solved = old_solved[contest_id]
            elif contest.solved == 0:
                contest.solved = sum(1 for task in contest.tasks if task.path is not None or (contest.div == "ABC" and task.label in {"A", "B", "C"}))
    return contests


def apply_statuses(contests: dict[str, Contest], old_statuses: dict[str, dict[str, str]]) -> None:
    for contest in contests.values():
        old = old_statuses.get(contest.contest, {})
        solved_labels = {
            task.label
            for task in sorted(contest.tasks, key=lambda task: label_sort_key(task.label))[: max(contest.solved, 0)]
        }
        for task in contest.tasks:
            if contest.missed:
                task.status = ""
            elif task.label in solved_labels:
                task.status = CHECK
            elif old.get(task.label) and old[task.label] not in {"B", "-"}:
                value = old[task.label]
                task.status = CHECK if value.startswith(CHECK) else value
            elif contest.div == "ABC" and task.label in {"A", "B", "C"}:
                task.status = CHECK
            elif task.path is not None:
                task.status = "B"
            else:
                task.status = ""


def clean_code(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = []
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("#"):
            continue
        if re.fullmatch(r"using\s+namespace\s+std\s*;", stripped):
            continue
        lines.append(raw_line.rstrip())
    text = "\n".join(lines)
    pattern = re.compile(r"(?m)^\s*(?:int|signed|void)\s+main\s*\(")
    while True:
        match = pattern.search(text)
        if not match:
            break
        brace = text.find("{", match.end())
        if brace == -1:
            break
        depth = 0
        end = None
        for index in range(brace, len(text)):
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
                if depth == 0:
                    end = index + 1
                    break
        if end is None:
            break
        text = text[: match.start()] + text[end:]
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def write_main(path: Path, contests: list[Contest]) -> None:
    labels = sorted({task.label for contest in contests for task in contest.tasks}, key=label_sort_key)
    lines = [
        "---",
        f"title: {SERIES_TITLE}",
        "date: 2025-01-21",
        "encrypt: true",
        'image: "/images/anime-diary/6.jpg"',
        "categories:",
        "    - 算法",
        "updates:",
        "    - date: 2026-07-17",
        "      content: 移除已停用的独立比赛页入口。",
        "    - date: 2026-06-25",
        "      content: 同步 Shiro_neko 的 AtCoder 官方记录，按官方过题数区分赛时通过与赛后补题。",
        "    - date: 2026-05-28",
        "      content: 新增 AtCoder 复盘表格，并同步官方排名、Performance 与赛时/补题状态。",
        "seriesExclude: true",
        "---",
        "## 前言",
        "这一篇用来放 AtCoder 的长期复盘。ABC 的 A、B、C 也会标记为赛时通过，只是题解页里仍然只保留真正需要回看的题目；表格中的 `√` 表示赛时通过，`B` 表示赛后补题。",
        "",
        "## 比赛记录",
        "| Date | Round | div | id | sol | rk | perf | " + " | ".join(labels) + " |",
        "| ---- | ----- | --- | -- | --- | -- | ---- | " + " | ".join("-" for _ in labels) + " |",
    ]
    for contest in contests:
        task_by_label = {task.label: task.status for task in contest.tasks}
        cells = [task_by_label.get(label, "") for label in labels]
        ref = '{{< ref "' + contest.ref + '" >}}'
        lines.append(
            "| {date} | [{round}]({ref}) | {div} | [{contest}]({url}) | {solved} | {rank} | {perf} | {tasks} |".format(
                date=contest.date.replace("-", "."),
                round=contest.round,
                ref=ref,
                div=contest.div,
                contest=contest.contest,
                url=contest.url,
                solved=contest.solved,
                rank=contest.rank,
                perf=contest.perf,
                tasks=" | ".join(cells),
            )
        )
    lines.extend(["", "## 复盘入口"])
    for contest in contests:
        lines.extend(["", f'[{contest.title}]({{{{< ref "{contest.ref}" >}}}})'])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def should_skip_child_task(contest: Contest, label: str) -> bool:
    return contest.div == "ABC" and label in {"A", "B"}


def prune_child_page(base_dir: Path, contest: Contest) -> bool:
    path = base_dir / contest.ref
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    matches = list(re.finditer(r"(?m)^##\s+\S+\s+([A-Z]\d*)\b.*$", text))
    if not matches:
        return False

    pieces: list[str] = []
    cursor = 0
    changed = False
    for index, match in enumerate(matches):
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        label = match.group(1)
        if should_skip_child_task(contest, label):
            pieces.append(text[cursor : match.start()])
            cursor = next_start
            changed = True
    if not changed:
        return False

    pieces.append(text[cursor:])
    new_text = re.sub(r"\n{3,}", "\n\n", "".join(pieces)).rstrip() + "\n"
    path.write_text(new_text, encoding="utf-8")
    return True


def write_child_pages(base_dir: Path, contests: list[Contest]) -> list[str]:
    base_dir.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    for order, contest in enumerate(contests, 1):
        path = base_dir / contest.ref
        if path.exists():
            continue
        lines = [
            "---",
            f'title: "{contest.title}"',
            f"slug: {Path(contest.ref).stem}",
            f"date: {contest.date}",
            f"seriesOrder: {order}",
            "encrypt: false",
            "hidden: true",
            f'image: "{DEFAULT_IMAGE}"',
            "---",
            "",
        ]
        for task in contest.tasks:
            if should_skip_child_task(contest, task.label):
                continue
            lines.extend(
                [
                    f"## {contest.round} {task.label}",
                    f"出处：[{contest.round} {task.label}]({task.url})",
                    "",
                    "题目大意：",
                    "",
                    "数据范围：",
                    "",
                    "思路：",
                    "",
                ]
            )
            if task.path is not None:
                lines.extend(["```cpp", clean_code(task.path), "```", ""])
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        created.append(contest.ref)
    for contest in contests:
        prune_child_page(base_dir, contest)
    return created


def sync(cp_root: Path, handle: str) -> None:
    old_statuses, old_solved = parse_old_statuses(SERIES_DIR / "main.md")
    cp_contests = discover_cp(cp_root)
    history = fetch_history(handle)
    contests_by_id = merge_history(cp_contests, history, old_solved)
    apply_statuses(contests_by_id, old_statuses)
    contests = sorted(contests_by_id.values(), key=lambda contest: (contest.date, contest.contest))
    visible_contests = [contest for contest in contests if not contest.missed]

    write_main(SERIES_DIR / "main.md", visible_contests)
    created = write_child_pages(SERIES_DIR, visible_contests)

    missed = [contest for contest in contests if contest.missed]
    print(
        f"records={len(visible_contests)} cp={len(cp_contests)} "
        f"history={len(history)} created_pages={len(created)} skipped_missed={len(missed)}"
    )
    for contest in missed:
        print(f"missed {contest.round} {contest.contest} rank={contest.rank} perf={contest.perf}")
    for ref in created:
        print(f"created {ref}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cp-root", type=Path, default=DEFAULT_CP_ROOT)
    parser.add_argument("--handle", default=DEFAULT_HANDLE)
    args = parser.parse_args()
    sync(args.cp_root, args.handle)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
