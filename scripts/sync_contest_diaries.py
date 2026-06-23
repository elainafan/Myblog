#!/usr/bin/env python3
"""Sync AtCoder and XCPC diary pages from the local Contests repository."""

from __future__ import annotations

import argparse
import gzip
import html as html_lib
import http.cookiejar
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BLOG_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTESTS_ROOT = Path(__file__).resolve().parents[3] / "Contests"
ATCODER_HANDLE = "Shiro_neko"
ATCODER_SERIES_DIR = "AtCoder修炼日记！"
XCPC_SERIES_DIR = "XCPC修炼日记！"
DEFAULT_IMAGE = "/images/anime-diary/5.png"

ATCODER_KIND_NAME = {
    "ABC": "AtCoder Beginner Contest",
    "ARC": "AtCoder Regular Contest",
}

XCPC_META = {
    "23GDCPC": {
        "date": "2023-05-14",
        "round": "23GDCPC",
        "title": "2023 广东省大学生程序设计竞赛",
        "contest": "104369",
        "div": "省赛",
        "group": "province",
        "url": "https://codeforces.com/gym/104369",
        "ref": "gdcpc-2023.md",
        "members": ["PaperMemory", "Kuro_neko"],
        "team": "Linger_Big_Pig",
        "rank": "30",
        "penalty": "674",
    }
}


@dataclass
class Task:
    label: str
    path: Path | None
    problem_id: str
    url: str
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
    rank: str = "vp"
    perf: str = "vp"
    penalty: str = ""
    team: str = ""
    members: list[str] | None = None
    rating: str = ""
    solved: int = 0
    order: int = 0


def request_json(url: str, timeout: int = 20) -> Any:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0 (hugo contest sync; +https://www.elainafan.one/)",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = response.read()
        if response.headers.get("Content-Encoding") == "gzip":
            payload = gzip.decompress(payload)
    data = json.loads(payload.decode("utf-8"))
    if isinstance(data, dict) and data.get("message") == "Forbidden":
        raise urllib.error.HTTPError(url, 403, "Forbidden", {}, None)
    return data


def parse_atcoder_time(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def epoch_seconds(dt: datetime | None) -> int | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def yaml_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return json.dumps("" if value is None else str(value), ensure_ascii=False)


def write_yaml(path: Path, contests: list[Contest], generated_by: str) -> None:
    lines = [
        f"generated_by: {yaml_value(generated_by)}",
        "contests:",
    ]
    for contest in contests:
        lines.extend(
            [
                f"  - date: {yaml_value(contest.date)}",
                f"    round: {yaml_value(contest.round)}",
                f"    title: {yaml_value(contest.title)}",
                f"    div: {yaml_value(contest.div)}",
                f"    group: {yaml_value(contest.group)}",
                f"    contest: {yaml_value(contest.contest)}",
                f"    url: {yaml_value(contest.url)}",
                f"    solved: {yaml_value(contest.solved)}",
                f"    rank: {yaml_value(contest.rank)}",
            ]
        )
        if contest.perf:
            lines.append(f"    perf: {yaml_value(contest.perf)}")
        if contest.penalty:
            lines.append(f"    penalty: {yaml_value(contest.penalty)}")
        if contest.team:
            lines.append(f"    team: {yaml_value(contest.team)}")
        if contest.rating:
            lines.append(f"    rating: {yaml_value(contest.rating)}")
        lines.append(f"    ref: {yaml_value(contest.ref)}")
        if contest.penalty:
            lines.append(f"    problems: {yaml_value(problem_text(contest.tasks))}")
        else:
            lines.append(f"    status: {yaml_value(status_text(contest.tasks))}")
        lines.append("    tasks:")
        for task in contest.tasks:
            lines.extend(
                [
                    f"      - label: {yaml_value(task.label)}",
                    f"        problem: {yaml_value(task.problem_id)}",
                    f"        status: {yaml_value(task.status)}",
                    f"        url: {yaml_value(task.url)}",
                ]
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def status_text(tasks: list[Task]) -> str:
    return " ".join(f"{task.label}{task.status or '-'}" for task in tasks)


def problem_text(tasks: list[Task]) -> str:
    return " / ".join(task.label for task in tasks)


def label_sort_key(label: str) -> tuple[str, int]:
    match = re.fullmatch(r"([A-Z]+)(\d*)", label)
    if not match:
        return (label, 0)
    head, tail = match.groups()
    return (head, int(tail or 0))


def problem_sort_key(path: Path) -> tuple[str, str]:
    stem = path.stem
    match = re.search(r"([A-Za-z]\d*)$", stem)
    return (*label_sort_key(match.group(1).upper() if match else stem.upper()), stem)


def remove_function(text: str, match: re.Match[str]) -> str:
    brace = text.find("{", match.end())
    if brace == -1:
        return text
    depth = 0
    for index in range(brace, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[: match.start()] + text[index + 1 :]
    return text


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
        next_text = remove_function(text, match)
        if next_text == text:
            break
        text = next_text
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    solve_match = re.search(r"(?m)^\s*void\s+solve\s*\(", text)
    if not solve_match:
        return text
    return text


def atcoder_problem_url(contest_id: str, label: str) -> str:
    return f"https://atcoder.jp/contests/{contest_id}/tasks/{contest_id}_{label.lower()}"


def discover_atcoder(contests_root: Path) -> list[Contest]:
    base = contests_root / "Atcoder"
    contests: list[Contest] = []
    if not base.exists():
        return contests
    for directory in sorted(base.glob("*/*")):
        if not directory.is_dir():
            continue
        match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})\s+([A-Z]+)(\d+)", directory.name)
        if not match:
            continue
        date, kind, number = match.groups()
        contest_id = f"{kind.lower()}{number}"
        all_files = sorted(directory.glob("*.cpp"), key=problem_sort_key)
        tasks: list[Task] = []
        if kind == "ABC":
            for label in ("A", "B", "C"):
                tasks.append(
                    Task(
                        label=label,
                        path=None,
                        problem_id=f"{contest_id}_{label.lower()}",
                        url=atcoder_problem_url(contest_id, label),
                    )
                )
        for path in all_files:
            label_match = re.search(r"([A-Za-z]\d*)$", path.stem)
            if not label_match:
                continue
            label = label_match.group(1).upper()
            if kind == "ABC" and label in {"A", "B", "C"}:
                continue
            tasks.append(
                Task(
                    label=label,
                    path=path,
                    problem_id=f"{contest_id}_{label.lower()}",
                    url=atcoder_problem_url(contest_id, label),
                )
            )
        if not tasks:
            continue
        round_name = f"{kind}{number}"
        title_prefix = ATCODER_KIND_NAME.get(kind, "AtCoder Contest")
        contests.append(
            Contest(
                date=date,
                round=round_name,
                title=f"{title_prefix} {number}",
                div=kind,
                group=kind.lower(),
                contest=contest_id,
                url=f"https://atcoder.jp/contests/{contest_id}",
                ref=f"{kind.lower()}-{number}.md",
                tasks=tasks,
            )
        )
    return contests


def sync_atcoder_official(contests: list[Contest], handle: str) -> None:
    if not contests:
        return
    contest_ids = {contest.contest for contest in contests}
    first_date = min(contest.date for contest in contests)
    first_dt = datetime.fromisoformat(f"{first_date}T00:00:00+09:00")
    from_second = max(0, int(first_dt.timestamp()) - 60 * 60 * 24 * 30)

    history_url = f"https://atcoder.jp/users/{handle}/history/json"
    submissions_url = (
        "https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions"
        f"?user={handle}&from_second={from_second}"
    )

    try:
        history = request_json(history_url)
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] failed to fetch AtCoder history: {exc}", file=sys.stderr)
        history = []

    history_by_id: dict[str, dict[str, Any]] = {}
    for item in history:
        screen = str(item.get("ContestScreenName", "")).split(".", 1)[0]
        if screen in contest_ids:
            history_by_id[screen] = item

    try:
        submissions = request_json(submissions_url)
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] failed to fetch AtCoder submissions: {exc}", file=sys.stderr)
        submissions = []

    first_ac: dict[str, int] = {}
    for item in submissions:
        if item.get("result") != "AC":
            continue
        contest_id = str(item.get("contest_id", ""))
        if contest_id not in contest_ids:
            continue
        problem_id = str(item.get("problem_id", ""))
        epoch = int(item.get("epoch_second", 0) or 0)
        if not problem_id or epoch <= 0:
            continue
        first_ac[problem_id] = min(first_ac.get(problem_id, epoch), epoch)

    for contest in contests:
        official = history_by_id.get(contest.contest, {})
        if official:
            contest.rank = str(official.get("Place", "vp"))
            contest.perf = str(official.get("Performance", "vp"))
            contest.rating = str(official.get("NewRating", ""))
            end_epoch = epoch_seconds(parse_atcoder_time(str(official.get("EndTime", ""))))
        else:
            end_epoch = None

        contest_all_ac = {
            problem_id: epoch
            for problem_id, epoch in first_ac.items()
            if problem_id.startswith(f"{contest.contest}_")
        }
        if end_epoch is not None:
            contest.solved = sum(1 for epoch in contest_all_ac.values() if epoch <= end_epoch)
        else:
            contest.solved = len(contest_all_ac)

        for task in contest.tasks:
            epoch = first_ac.get(task.problem_id)
            if epoch is None:
                task.status = "B"
            elif end_epoch is not None and epoch <= end_epoch:
                task.status = "√"
            else:
                task.status = "B"


def request_cf_gym_standings(contest_id: str, timeout: int = 20) -> str:
    url = f"https://mirror.codeforces.com/gym/{contest_id}/standings"
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    headers = {"User-Agent": "Mozilla/5.0 (hugo contest sync; +https://www.elainafan.one/)"}

    page = opener.open(urllib.request.Request(url, headers=headers), timeout=timeout).read().decode(
        "utf-8",
        "ignore",
    )
    csrf_match = re.search(r"name='csrf_token' value='([^']+)'", page)
    if not csrf_match:
        return page

    payload = urllib.parse.urlencode(
        {
            "csrf_token": csrf_match.group(1),
            "action": "toggleShowUnofficial",
            "newShowUnofficialValue": "true",
            "showUnofficial": "on",
        }
    ).encode()
    return opener.open(
        urllib.request.Request(
            url,
            data=payload,
            headers={**headers, "Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        ),
        timeout=timeout,
    ).read().decode("utf-8", "ignore")


def cell_text(cell: str) -> str:
    text = html_lib.unescape(re.sub(r"<[^>]+>", " ", cell))
    return re.sub(r"\s+", " ", text).strip()


def apply_xcpc_row(contest: Contest, row: str) -> bool:
    raw_cells = [match.group(0) for match in re.finditer(r"<t[dh][^>]*>[\s\S]*?</t[dh]>", row)]
    cells = [cell_text(cell) for cell in raw_cells]
    if len(cells) < 4:
        return False

    contest.rank = cells[0]
    contestant = cells[1].split("#", 1)[0].strip()
    contest.team = contestant.split(":", 1)[0].strip() or contest.team
    contest.solved = int(cells[2]) if cells[2].isdigit() else contest.solved
    contest.penalty = cells[3]

    problem_cells = raw_cells[4:]
    for task in contest.tasks:
        problem_index = ord(task.label[0]) - ord("A")
        if 0 <= problem_index < len(problem_cells) and "cell-accepted" in problem_cells[problem_index]:
            task.status = "√"
    return True


def sync_xcpc_official(contests: list[Contest]) -> None:
    for contest in contests:
        handles = contest.members or []
        if not handles and not contest.team:
            continue
        found = False
        for _ in range(8):
            try:
                page = request_cf_gym_standings(contest.contest)
            except Exception as exc:  # noqa: BLE001
                print(f"[warn] failed to fetch Codeforces Gym standings: {exc}", file=sys.stderr)
                break
            for match in re.finditer(r"<tr\b[\s\S]*?</tr>", page):
                row = match.group(0)
                if all(handle in row for handle in handles) or (not handles and contest.team in row):
                    apply_xcpc_row(contest, row)
                    found = True
                    break
            if found:
                break
        if not found:
            target = ", ".join(handles) if handles else contest.team
            print(f"[warn] standings row not found for {contest.round}: {target}", file=sys.stderr)


def discover_xcpc(contests_root: Path) -> list[Contest]:
    base = contests_root / "XCPC"
    contests: list[Contest] = []
    if not base.exists():
        return contests
    for directory in sorted(path for path in base.glob("*/*") if path.is_dir()):
        meta = XCPC_META.get(directory.name)
        files = sorted(directory.glob("*.cpp"), key=problem_sort_key)
        if not files:
            continue
        contest_id = meta["contest"] if meta else re.match(r"(\d+)", files[0].stem).group(1)
        tasks: list[Task] = []
        for path in files:
            label_match = re.search(r"([A-Z]\d*)$", path.stem)
            if not label_match:
                continue
            label = label_match.group(1).upper()
            tasks.append(
                Task(
                    label=label,
                    path=path,
                    problem_id=f"{contest_id}{label}",
                    url=f"https://codeforces.com/gym/{contest_id}/problem/{label}",
                    status="B",
                )
            )
        if not tasks:
            continue
        contests.append(
            Contest(
                date=meta["date"] if meta else "2023-01-01",
                round=meta["round"] if meta else directory.name,
                title=meta["title"] if meta else directory.name,
                div=meta["div"] if meta else directory.parent.name,
                group=meta["group"] if meta else "xcpc",
                contest=contest_id,
                url=meta["url"] if meta else f"https://codeforces.com/gym/{contest_id}",
                ref=meta["ref"] if meta else f"{directory.name.lower()}.md",
                tasks=tasks,
                rank=meta.get("rank", "vp") if meta else "vp",
                perf=meta.get("perf", "") if meta else "",
                penalty=meta.get("penalty", "") if meta else "",
                team=meta.get("team", "") if meta else "",
                members=list(meta.get("members", [])) if meta else None,
                solved=len(tasks),
            )
        )
    return contests


def frontmatter(title: str, date: str, extra: list[str] | None = None) -> str:
    lines = [
        "---",
        f"title: {title}",
        f"date: {date}",
        f'image: "{DEFAULT_IMAGE}"',
        "categories:",
        "    - 算法",
    ]
    if extra:
        lines.extend(extra)
    lines.append("---")
    return "\n".join(lines)


def write_main_article(path: Path, title: str, date: str, intro: str, contests: list[Contest], update: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    is_xcpc = any(contest.penalty or contest.team for contest in contests)
    task_columns = list("ABCDEFGHIJKLMN") if is_xcpc else sorted(
        {task.label for contest in contests for task in contest.tasks},
        key=label_sort_key,
    )
    lines = [
        frontmatter(
            title,
            date,
            [
                "updates:",
                "    - date: 2026-05-28",
                f"      content: {update}",
                "seriesExclude: true",
            ],
        ),
        "## 前言",
        intro,
        "",
        "## 比赛记录",
    ]
    if is_xcpc:
        lines.extend(
            [
                "| Date | Round | div | id | team | sol | rank | penalty | "
                + " | ".join(task_columns)
                + " |",
                "| ---- | ----- | --- | -- | ---- | --- | ---- | ------- | "
                + " | ".join("-" for _ in task_columns)
                + " |",
            ]
        )
    else:
        lines.extend(
            [
                "| Date | Round | div | id | sol | rk | perf | "
                + " | ".join(task_columns)
                + " |",
                "| ---- | ----- | --- | -- | --- | -- | ---- | "
                + " | ".join("-" for _ in task_columns)
                + " |",
            ]
        )
    for contest in sorted(contests, key=lambda item: item.date):
        ref = f'{{{{< ref "{contest.ref}" >}}}}'
        task_by_label = {task.label: task.status for task in contest.tasks}
        task_cells = [task_by_label.get(label, "") for label in task_columns]
        if is_xcpc:
            lines.append(
                "| {date} | [{round}]({ref}) | {div} | [{contest}]({url}) | {team} | {solved} | {rank} | {penalty} | {tasks} |".format(
                    date=contest.date.replace("-", "."),
                    round=contest.round,
                    ref=ref,
                    div=contest.div,
                    contest=contest.contest,
                    url=contest.url,
                    team=contest.team or "-",
                    solved=contest.solved,
                    rank=contest.rank,
                    penalty=contest.penalty or "-",
                    tasks=" | ".join(task_cells),
                )
            )
        else:
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
                    tasks=" | ".join(task_cells),
                )
            )
    lines.extend(["", "## 复盘入口"])
    for contest in sorted(contests, key=lambda item: item.date):
        lines.append("")
        lines.append(f'[{contest.title}]({{{{< ref "{contest.ref}" >}}}})')
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_child_pages(base_dir: Path, contests: list[Contest]) -> None:
    base_dir.mkdir(parents=True, exist_ok=True)
    for order, contest in enumerate(sorted(contests, key=lambda item: item.date), 1):
        contest.order = order
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
            if task.path is None:
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
                    "```cpp",
                    clean_code(task.path),
                    "```",
                    "",
                ]
            )
        (base_dir / contest.ref).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_page(path: Path, title: str, layout: str, url: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"""---
title: "{title}"
date: 2026-05-28
layout: "{layout}"
slug: "{layout}"
url: "{url}"
comments: false
---
"""
    path.write_text(content, encoding="utf-8")


def ensure_series_entries(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    blocks = []
    if "AtCoder 复盘" not in text:
        blocks.append(
            """
- title: AtCoder 复盘
  badge: ATC
  color: "#59a8ff"
  directory: post/AtCoder修炼日记！/
  home: post/AtCoder修炼日记！/main.md
  includeHidden: true
  dashboard: /series/atcoder/
  description: 长期更新的 AtCoder 比赛复盘，自动同步官方排名、Performance 与赛时/补题状态。
  preview: 5
"""
        )
    if "XCPC VP 记录" not in text:
        blocks.append(
            """
- title: XCPC VP 记录
  badge: XCPC
  color: "#f2c86b"
  directory: post/XCPC修炼日记！/
  home: post/XCPC修炼日记！/main.md
  includeHidden: true
  dashboard: /series/xcpc/
  description: 省赛、区域赛和训练赛的 VP 复盘入口，用同一套题解骨架记录补题过程。
  preview: 5
"""
        )
    if blocks:
        path.write_text(text.rstrip() + "\n\n" + "\n".join(block.strip() for block in blocks) + "\n", encoding="utf-8")


def sync(contests_root: Path, handle: str) -> None:
    atcoder = discover_atcoder(contests_root)
    sync_atcoder_official(atcoder, handle)
    xcpc = discover_xcpc(contests_root)
    sync_xcpc_official(xcpc)

    write_yaml(BLOG_ROOT / "data" / "atcoder.yaml", sorted(atcoder, key=lambda item: item.date), "scripts/sync_contest_diaries.py")
    write_yaml(BLOG_ROOT / "data" / "xcpc.yaml", sorted(xcpc, key=lambda item: item.date), "scripts/sync_contest_diaries.py")

    write_main_article(
        BLOG_ROOT / "content" / "post" / ATCODER_SERIES_DIR / "main.md",
        "放学后喝茶日记！",
        "2025-01-21",
        "这一篇用来放 AtCoder 的长期复盘。ABC 的 A、B、C 也会标记为赛时通过，只是题解页里仍然只保留真正需要回看的题目；表格中的 `√` 表示赛时通过，`B` 表示赛后补题。",
        atcoder,
        "新增 AtCoder 复盘表格，并同步官方排名、Performance 与赛时/补题状态。",
    )
    write_main_article(
        BLOG_ROOT / "content" / "post" / XCPC_SERIES_DIR / "main.md",
        "社团合宿作战手册！",
        "2025-01-21",
        "这一篇用来放 XCPC 相关的 VP 和补题记录。先把已经整理在本地仓库里的代码接进博客，之后补题时只需要继续填题目大意、数据范围和思路。",
        xcpc,
        "新增 XCPC VP 复盘入口，并按本地 Contests 仓库生成题解骨架。",
    )
    write_child_pages(BLOG_ROOT / "content" / "post" / ATCODER_SERIES_DIR, atcoder)
    write_child_pages(BLOG_ROOT / "content" / "post" / XCPC_SERIES_DIR, xcpc)
    write_page(BLOG_ROOT / "content" / "page" / "atcoder" / "index.md", "AtCoder", "atcoder", "/series/atcoder/")
    write_page(BLOG_ROOT / "content" / "page" / "xcpc" / "index.md", "XCPC", "xcpc", "/series/xcpc/")
    ensure_series_entries(BLOG_ROOT / "data" / "series.yaml")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contests-root", type=Path, default=DEFAULT_CONTESTS_ROOT)
    parser.add_argument("--atcoder-handle", default=ATCODER_HANDLE)
    args = parser.parse_args()
    sync(args.contests_root, args.atcoder_handle)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
