#!/usr/bin/env python3
"""Sync Codeforces diary from official PaperMemory / Kuro_neko records.

Rated contests use official rank plus estimated performance. Unrated official
contests are marked as ``unrated``. Existing or local CP-only records are kept
as VP records, and both rank/perf are written as ``vp``.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from sync_codeforces import (
    CHECK,
    CODEFORCES_DATA,
    CODEFORCES_MAIN,
    MANUAL_MARKERS,
    TASK_COLUMNS,
    estimate_performance,
    parse_existing_table,
    parse_simple_yaml,
    problem_sort_key,
    request_json,
    write_codeforces_yaml,
)


BLOG_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CP_ROOT = BLOG_ROOT.parents[1] / "CP" / "Codeforces"
DEFAULT_HANDLES = ("PaperMemory", "Kuro_neko")
DEFAULT_IMAGE = "/images/anime-diary/5.png"
CONTEST_PROBLEMS_CACHE: dict[str, dict[str, str]] = {}

FIELD_PROBLEM = "\u9898\u76ee\u5927\u610f\uff1a"
FIELD_RANGE = "\u6570\u636e\u8303\u56f4\uff1a"
FIELD_IDEA = "\u601d\u8def\uff1a"
HEADING_TABLE = "## \u770b\u756a\u65e5\u8bb0"
HEADING_REVIEW = "## \u6bd4\u8d5b\u590d\u76d8"
UPDATE_NOTE = (
    "      content: \u540c\u6b65 PaperMemory \u4e0e Kuro_neko "
    "\u7684\u5b98\u65b9\u53c2\u8d5b\u8bb0\u5f55\uff0c\u8865\u5145 "
    "Unrated / VP \u72b6\u6001\u548c\u8fd1\u671f\u573a\u6b21\u5165\u53e3\u3002"
)


@dataclass
class SourceTask:
    label: str
    path: Path
    contest_id: str


@dataclass
class CPContest:
    date: str
    short_round: str
    div_hint: str
    contest_id: str
    tasks: list[SourceTask]


@dataclass
class Official:
    handle: str
    rank: str
    perf: str
    solved: int
    accepted: set[str]
    submitted: set[str]


def series_dir() -> Path:
    post_dir = CODEFORCES_MAIN.parents[1]
    for child in post_dir.iterdir():
        if child.is_dir() and (child / "cf-1100.md").exists() and (child / "main.md").exists():
            return child
    raise RuntimeError("Codeforces diary directory not found")


def label_sort_key(label: str) -> tuple[str, int]:
    match = re.fullmatch(r"([A-Z]+)(\d*)", label.upper())
    if not match:
        return (label.upper(), 0)
    head, tail = match.groups()
    return (head, int(tail or 0))


def file_problem_label(path: Path) -> str | None:
    match = re.match(r"^\d+([A-Za-z]\d*)", path.stem)
    if match:
        return match.group(1).upper()
    match = re.search(r"([A-Za-z]\d*)$", path.stem)
    return match.group(1).upper() if match else None


def discover_cp(root: Path) -> dict[str, CPContest]:
    contests: dict[str, CPContest] = {}
    if not root.exists():
        return contests
    for directory in sorted(path for path in root.iterdir() if path.is_dir()):
        match = re.match(r"(\d{4}-\d{2}-\d{2})\s+([^()]+)(?:\(([^)]*)\))?", directory.name)
        if not match:
            continue
        date, short_round, div_hint = match.groups()
        files = sorted(
            [path for path in directory.iterdir() if path.suffix.lower() in {".cpp", ".py"}],
            key=lambda path: label_sort_key(file_problem_label(path) or path.stem),
        )
        if not files:
            continue
        contest_match = re.match(r"(\d+)", files[0].stem)
        if not contest_match:
            continue
        contest_id = contest_match.group(1)
        tasks = []
        for path in files:
            label = file_problem_label(path)
            if label:
                task_contest_match = re.match(r"(\d+)", path.stem)
                task_contest_id = task_contest_match.group(1) if task_contest_match else contest_id
                tasks.append(SourceTask(label=label, path=path, contest_id=task_contest_id))
        if tasks:
            contests[contest_id] = CPContest(
                date=date,
                short_round=short_round.strip(),
                div_hint=(div_hint or "").strip(),
                contest_id=contest_id,
                tasks=tasks,
            )
    return contests


def short_round(name: str) -> str:
    if "Hello 2026" in name:
        return "Hello 2026"
    if "Good Bye 2025" in name:
        return "Gb 2025"
    match = re.search(r"Educational Codeforces Round (\d+)", name)
    if match:
        return "Edu" + match.group(1)
    match = re.search(r"Codeforces Global Round (\d+)", name)
    if match:
        return "GR" + match.group(1)
    match = re.search(r"Codeforces Round (?:#)?(\d+)", name)
    if match:
        return "R" + match.group(1)
    return name


def div_group(name: str) -> tuple[str, str]:
    lowered = name.lower()
    if "educational codeforces round" in lowered:
        return "edu", "edu"
    if "div. 1 + div. 2" in lowered or "div. 1 + 2" in lowered or "div. 1+2" in lowered:
        return "div1+2", "div12"
    match = re.search(r"Div\.\s*(\d)", name)
    if match:
        div = "div" + match.group(1)
        return div, div
    if "global round" in lowered or "good bye" in lowered or "hello" in lowered:
        return "div1+2", "div12"
    return "", "other"


def div_from_cp(hint: str) -> tuple[str, str]:
    compact = hint.lower().replace("div.", "div").replace(" ", "")
    if compact in {"div1+2", "div1+div2"}:
        return "div1+2", "div12"
    if compact in {"div1", "div2", "div3", "div4"}:
        return compact, compact
    return "", "other"


def ref_for(round_name: str) -> str:
    if re.fullmatch(r"R\d+", round_name):
        return "cf-" + round_name[1:] + ".md"
    if re.fullmatch(r"Edu\d+", round_name):
        return "edu-" + round_name[3:] + ".md"
    if re.fullmatch(r"GR\d+", round_name):
        return "gr-" + round_name[2:] + ".md"
    if round_name == "Hello 2026":
        return "hello-2026.md"
    if round_name == "Gb 2025":
        return "gb-2025.md"
    slug = re.sub(r"[^a-z0-9]+", "-", round_name.lower()).strip("-")
    return slug + ".md"


def title_for(record: dict[str, str], fallback: str = "") -> str:
    round_name = record.get("round", "")
    div = record.get("div", "")
    if re.fullmatch(r"R\d+", round_name):
        number = round_name[1:]
        if div == "div1+2":
            return f"Codeforces Round #{number}(Div.1+2)"
        if div.startswith("div") and div[3:].isdigit():
            return f"Codeforces Round #{number}(Div.{div[3:]})"
        return f"Codeforces Round #{number}"
    if re.fullmatch(r"Edu\d+", round_name):
        return f"Educational Codeforces Round #{round_name[3:]}"
    if re.fullmatch(r"GR\d+", round_name):
        return f"Codeforces Global Round #{round_name[2:]}"
    if round_name == "Gb 2025":
        return "Good Bye 2025"
    return fallback or round_name


def fetch_official(handles: tuple[str, ...]) -> tuple[dict[str, Any], dict[str, Official]]:
    contests = request_json("contest.list", gym="false")
    meta = {str(item["id"]): item for item in contests if item.get("phase") == "FINISHED"}

    rating_by_contest: dict[str, tuple[str, dict[str, Any]]] = {}
    for handle in handles:
        for item in request_json("user.rating", handle=handle):
            rating_by_contest.setdefault(str(item["contestId"]), (handle, item))
        time.sleep(0.35)

    grouped: dict[str, dict[str, Any]] = {}
    for handle in handles:
        start = 1
        count = 10000
        while True:
            page = request_json("user.status", handle=handle, **{"from": start, "count": count})
            for submission in page:
                author = submission.get("author", {})
                if author.get("participantType") != "CONTESTANT":
                    continue
                contest_id = submission.get("contestId")
                if contest_id is None or str(contest_id) not in meta:
                    continue
                record = grouped.setdefault(
                    str(contest_id),
                    {"handle": handle, "accepted": set(), "submitted": set()},
                )
                # PaperMemory has priority if both handles appear in one contest.
                if record["handle"] != handle:
                    continue
                index = str(submission.get("problem", {}).get("index", ""))
                if not index:
                    continue
                record["submitted"].add(index)
                if submission.get("verdict") == "OK":
                    record["accepted"].add(index)
            if len(page) < count:
                break
            start += count
            time.sleep(0.35)
        time.sleep(0.35)

    official: dict[str, Official] = {}
    for contest_id, record in sorted(grouped.items(), key=lambda item: int(item[0])):
        if contest_id in rating_by_contest:
            handle, rating = rating_by_contest[contest_id]
            perf = estimate_performance(contest_id, handle)
            time.sleep(0.35)
            official[contest_id] = Official(
                handle=handle,
                rank=str(rating["rank"]),
                perf=perf,
                solved=len(record["accepted"]),
                accepted=set(record["accepted"]),
                submitted=set(record["submitted"]),
            )
        else:
            official[contest_id] = Official(
                handle=record["handle"],
                rank="unrated",
                perf="unrated",
                solved=len(record["accepted"]),
                accepted=set(record["accepted"]),
                submitted=set(record["submitted"]),
            )
    return meta, official


def fetch_problem_columns(contest_id: str, known_labels: set[str]) -> dict[str, str]:
    if not any(re.search(r"\d", label) for label in known_labels):
        return {label: label[:1] for label in known_labels if label[:1] in TASK_COLUMNS}
    labels = sorted(known_labels, key=problem_sort_key)
    return {label: TASK_COLUMNS[index] for index, label in enumerate(labels[: len(TASK_COLUMNS)])}


def fetch_contest_problems(contest_id: str) -> dict[str, str]:
    if contest_id not in CONTEST_PROBLEMS_CACHE:
        result = request_json("contest.standings", contestId=contest_id)
        CONTEST_PROBLEMS_CACHE[contest_id] = {
            str(problem.get("index", "")): str(problem.get("name", ""))
            for problem in result.get("problems", [])
            if problem.get("index") and problem.get("name")
        }
        time.sleep(0.35)
    return CONTEST_PROBLEMS_CACHE[contest_id]


def normalize_problem_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", name.lower())


def paired_div2_contest_id(record: dict[str, str], source: CPContest | None, meta: dict[str, Any]) -> str | None:
    contest_id = str(record.get("contest", ""))
    if source:
        for task in source.tasks:
            if task.contest_id != contest_id:
                return task.contest_id

    round_name = str(record.get("round", ""))
    match = re.fullmatch(r"R(\d+)", round_name)
    if not match:
        return None
    needle = f"Codeforces Round {match.group(1)}"
    for candidate_id, contest in meta.items():
        name = str(contest.get("name", ""))
        lowered = name.lower()
        if candidate_id != contest_id and needle in name and "div. 2" in lowered:
            return str(candidate_id)
    return None


def div1_to_div2_columns(
    record: dict[str, str],
    source: CPContest | None,
    meta: dict[str, Any],
) -> dict[str, str]:
    if str(record.get("div", "")).lower() != "div1":
        return {}
    div2_id = paired_div2_contest_id(record, source, meta)
    if not div2_id:
        return {}

    div1_problems = fetch_contest_problems(str(record["contest"]))
    div2_problems = fetch_contest_problems(div2_id)
    div2_by_name = {
        normalize_problem_name(name): problem_head(index)
        for index, name in div2_problems.items()
        if problem_head(index) in TASK_COLUMNS
    }
    return {
        index: div2_by_name[normalize_problem_name(name)]
        for index, name in div1_problems.items()
        if normalize_problem_name(name) in div2_by_name
    }


def table_column_for_source_task(
    record: dict[str, str],
    task: SourceTask,
    problem_columns: dict[str, str],
    div1_mapping: dict[str, str],
) -> str:
    if str(record.get("div", "")).lower() == "div1":
        if task.contest_id == str(record.get("contest", "")):
            return div1_mapping.get(task.label, problem_head(task.label))
        return problem_head(task.label)
    return problem_columns.get(task.label, problem_head(task.label))


def table_column_for_problem_index(
    record: dict[str, str],
    label: str,
    problem_columns: dict[str, str],
    div1_mapping: dict[str, str],
) -> str:
    if str(record.get("div", "")).lower() == "div1":
        return div1_mapping.get(label, problem_head(label))
    return problem_columns.get(label, problem_head(label))


def remove_function(text: str, match: re.Match[str]) -> str:
    brace = text.find("{", match.end())
    if brace == -1:
        return text
    depth = 0
    for index in range(brace, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
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
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def problem_head(label: str) -> str:
    div_match = re.search(r"\bDiv\.\s*\d\s+([A-Z]\d*)\b", label, flags=re.I)
    if div_match:
        return div_match.group(1).upper()
    match = re.match(r"[A-Z]+", label.upper())
    return match.group(0) if match else label.upper()


def should_skip_child_problem(record: dict[str, str], label: str) -> bool:
    div = str(record.get("div", "")).lower()
    head = problem_head(label)
    if div == "div1" and re.search(r"\bDiv\.\s*2\s+A\b", label, flags=re.I):
        return True
    if div in {"div2", "edu", "div1+2"}:
        return head == "A"
    if div in {"div3", "div4"}:
        return head in {"A", "B", "C"}
    return False


def display_label_for_source(record: dict[str, str], task: SourceTask) -> str:
    if str(record.get("div", "")).lower() == "div1":
        prefix = "Div.1" if task.contest_id == str(record.get("contest", "")) else "Div.2"
        return f"{prefix} {task.label}"
    return task.label


def child_problem_label(label: str) -> str:
    div_match = re.search(r"\bDiv\.\s*\d\s+([A-Z]\d*)\b", label, flags=re.I)
    if div_match:
        return div_match.group(1).upper()
    match = re.match(r"([A-Z]\d*)", label.upper())
    return match.group(1) if match else label.upper()


def child_label_sort_key(record: dict[str, str], label: str) -> tuple[int, str, int]:
    group = 0
    if str(record.get("div", "")).lower() == "div1":
        if re.search(r"\bDiv\.\s*2\b", label, flags=re.I):
            group = 0
        elif re.search(r"\bDiv\.\s*1\b", label, flags=re.I):
            group = 1
        else:
            group = 2
    head, tail = label_sort_key(child_problem_label(label))
    return (group, head, tail)


def write_child_page(
    directory: Path,
    record: dict[str, str],
    source: CPContest | None,
    labels: list[str],
    series_order: int,
    meta_name: str,
) -> bool:
    path = directory / record["ref"]
    if path.exists():
        return False
    lines = [
        "---",
        f'title: "{title_for(record, meta_name)}"',
        f"slug: {Path(record['ref']).stem}",
        f"date: {record['date']}",
        f"seriesOrder: {series_order}",
        "encrypt: false",
        "hidden: true",
        f'image: "{DEFAULT_IMAGE}"',
        "---",
        "",
    ]
    task_paths = {display_label_for_source(record, task): task.path for task in source.tasks} if source else {}
    if source:
        labels = [display_label_for_source(record, task) for task in source.tasks]
    labels = [label for label in labels if not should_skip_child_problem(record, label)]
    labels = sorted(labels, key=lambda label: child_label_sort_key(record, label))
    for label in labels:
        lines.extend([f"## {label}", FIELD_PROBLEM, "", FIELD_RANGE, "", FIELD_IDEA, ""])
        code_path = task_paths.get(label)
        if code_path:
            language = "python" if code_path.suffix.lower() == ".py" else "cpp"
            lines.extend([f"```{language}", clean_code(code_path), "```", ""])
        else:
            lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return True


def prune_child_page(directory: Path, record: dict[str, str]) -> bool:
    path = directory / record["ref"]
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    matches = list(re.finditer(r"(?m)^##\s+((?:Div\.\s*\d\s+)?[A-Z]\d*)\b.*$", text))
    if not matches:
        return False

    pieces: list[str] = []
    cursor = 0
    changed = False
    for index, match in enumerate(matches):
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        label = match.group(1)
        if should_skip_child_problem(record, label):
            pieces.append(text[cursor : match.start()])
            cursor = next_start
            changed = True
    if not changed:
        return False

    pieces.append(text[cursor:])
    new_text = re.sub(r"\n{3,}", "\n\n", "".join(pieces)).rstrip() + "\n"
    path.write_text(new_text, encoding="utf-8")
    return True


def render_table(records: list[dict[str, str]], statuses: dict[str, dict[str, str]]) -> str:
    lines = [
        "| Date | Round | div | id | sol | rk | perf | " + " | ".join(TASK_COLUMNS) + " |",
        "| ---- | ----- | --- | -- | --- | -- | ---- | " + " | ".join("-" for _ in TASK_COLUMNS) + " |",
    ]
    for record in records:
        contest_id = record["contest"]
        ref = '{{< ref "' + record["ref"] + '" >}}'
        cells = [statuses.get(contest_id, {}).get(column, "") for column in TASK_COLUMNS]
        lines.append(
            "| {date} | [{round}]({ref}) | {div} | [{contest}](https://codeforces.com/contest/{contest}) | "
            "{solved} | {rank} | {perf} | {tasks} |".format(
                date=record["date"].replace("-", "."),
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


def replace_main(records: list[dict[str, str]], statuses: dict[str, dict[str, str]]) -> None:
    text = CODEFORCES_MAIN.read_text(encoding="utf-8")
    if "\u540c\u6b65 PaperMemory \u4e0e Kuro_neko \u7684\u5b98\u65b9\u53c2\u8d5b\u8bb0\u5f55" not in text:
        text = text.replace("updates:\n", "updates:\n    - date: 2026-06-25\n" + UPDATE_NOTE + "\n", 1)
    table = render_table(records, statuses)
    table_match = re.search(f"({HEADING_TABLE}\n)(.*?)(\n{HEADING_REVIEW})", text, flags=re.S)
    if not table_match:
        raise RuntimeError("Codeforces table block not found")
    text = text[: table_match.start(2)] + table + "\n" + text[table_match.start(3) :]
    review_lines = [HEADING_REVIEW]
    for record in records:
        review_lines.extend(["", f'[{title_for(record)}]({{{{< ref "{record["ref"]}" >}}}})'])
    text = re.sub(f"{HEADING_REVIEW}[\\s\\S]*$", "\n".join(review_lines) + "\n", text)
    CODEFORCES_MAIN.write_text(text, encoding="utf-8")


def record_date(record: dict[str, str], meta: dict[str, Any], cp: dict[str, CPContest], contest_id: str) -> str:
    if record.get("date"):
        return record["date"]
    if contest_id in meta:
        return datetime.fromtimestamp(meta[contest_id]["startTimeSeconds"], timezone.utc).astimezone(
            timezone(timedelta(hours=8))
        ).strftime("%Y-%m-%d")
    return cp[contest_id].date


def build_records(
    old_records: list[dict[str, str]],
    old_statuses: dict[str, dict[str, str]],
    cp: dict[str, CPContest],
    meta: dict[str, Any],
    official: dict[str, Official],
) -> tuple[list[dict[str, str]], dict[str, dict[str, str]], list[str], list[str]]:
    old_by_id = {str(record["contest"]): dict(record) for record in old_records}
    selected = set(old_by_id) | set(official) | set(cp)

    records: list[dict[str, str]] = []
    statuses: dict[str, dict[str, str]] = {}
    changes: list[str] = []

    for contest_id in sorted(selected, key=lambda cid: (record_date(old_by_id.get(cid, {}), meta, cp, cid), int(cid))):
        record = dict(old_by_id.get(contest_id, {}))
        meta_name = meta.get(contest_id, {}).get("name", "")
        if not record:
            if contest_id in meta:
                date = record_date({}, meta, cp, contest_id)
                round_name = short_round(meta_name)
                div, group = div_group(meta_name)
            else:
                date = cp[contest_id].date
                round_name = cp[contest_id].short_round
                div, group = div_from_cp(cp[contest_id].div_hint)
            record = {
                "date": date,
                "round": round_name,
                "div": div,
                "group": group,
                "contest": contest_id,
                "solved": "0",
                "rank": "vp",
                "perf": "vp",
                "ref": ref_for(round_name),
            }

        official_record = official.get(contest_id)
        before = (str(record.get("solved", "")), str(record.get("rank", "")), str(record.get("perf", "")))
        if official_record:
            record["solved"] = str(official_record.solved)
            record["rank"] = official_record.rank
            record["perf"] = official_record.perf
        else:
            record["rank"] = "vp"
            record["perf"] = "vp"
            if contest_id in cp and (
                not str(record.get("solved", "")).isdigit() or int(str(record.get("solved", "0") or "0")) == 0
            ):
                record["solved"] = str(len(cp[contest_id].tasks))
        after = (str(record.get("solved", "")), str(record.get("rank", "")), str(record.get("perf", "")))
        if before != after:
            changes.append(f"{record.get('round')} {contest_id}: {before} -> {after}")

        source = cp.get(contest_id)
        known = set()
        if source:
            known.update(task.label for task in source.tasks)
        if official_record:
            known.update(official_record.accepted)
            known.update(official_record.submitted)
        if not known:
            known.update(column for column, value in old_statuses.get(contest_id, {}).items() if value)
        div1_mapping = div1_to_div2_columns(record, source, meta)
        columns = {} if div1_mapping else fetch_problem_columns(contest_id, known) if known else {}
        source_columns = (
            {
                table_column_for_source_task(record, task, columns, div1_mapping)
                for task in source.tasks
                if table_column_for_source_task(record, task, columns, div1_mapping) in TASK_COLUMNS
            }
            if source
            else set()
        )
        official_columns = {
            table_column_for_problem_index(record, label, columns, div1_mapping)
            for label in (official_record.accepted if official_record else set())
            if table_column_for_problem_index(record, label, columns, div1_mapping) in TASK_COLUMNS
        }
        old = old_statuses.get(contest_id, {})
        row_status = {}
        is_div1 = str(record.get("div", "")).lower() == "div1"
        mapped_div1_columns = set(div1_mapping.values())
        for column in TASK_COLUMNS:
            old_value = old.get(column, "").strip()
            if not official_record and old_value and not is_div1:
                row_status[column] = old_value
                continue
            if column in official_columns:
                row_status[column] = CHECK
            elif column in source_columns:
                row_status[column] = old_value if old_value else "B"
            elif official_record and old_value == CHECK and not is_div1:
                row_status[column] = "B"
            elif is_div1 and column in mapped_div1_columns and old_value in (MANUAL_MARKERS | {CHECK}):
                row_status[column] = old_value
            elif old_value in (MANUAL_MARKERS - {"B"}) or (old_value == CHECK and not is_div1):
                row_status[column] = old_value
            else:
                row_status[column] = ""
        statuses[contest_id] = row_status
        records.append(record)
    return records, statuses, changes, sorted(selected)


def sync(cp_root: Path, handles: tuple[str, ...]) -> None:
    old_records = parse_simple_yaml(CODEFORCES_DATA)
    old_statuses = parse_existing_table(CODEFORCES_MAIN)
    cp = discover_cp(cp_root)
    meta, official = fetch_official(handles)
    records, statuses, changes, _ = build_records(old_records, old_statuses, cp, meta, official)

    directory = series_dir()
    created = []
    pruned = []
    order_map = {record["contest"]: index + 1 for index, record in enumerate(records)}
    for record in records:
        contest_id = record["contest"]
        source = cp.get(contest_id)
        official_record = official.get(contest_id)
        if source:
            labels = [task.label for task in source.tasks]
        elif official_record:
            labels = sorted(official_record.accepted or official_record.submitted, key=problem_sort_key)
        else:
            labels = []
        if write_child_page(directory, record, source, labels, order_map[contest_id], meta.get(contest_id, {}).get("name", "")):
            created.append(record["ref"])
        if prune_child_page(directory, record):
            pruned.append(record["ref"])

    write_codeforces_yaml(CODEFORCES_DATA, records)
    replace_main(records, statuses)
    print(
        f"records={len(records)} official={len(official)} "
        f"cp={len(cp)} "
        f"created_pages={len(created)} pruned_pages={len(pruned)}"
    )
    for page in created:
        print(f"created {page}")
    for page in pruned[:120]:
        print(f"pruned {page}")
    for change in changes[:120]:
        print(f"changed {change}")


def main() -> int:
    sync(DEFAULT_CP_ROOT, DEFAULT_HANDLES)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
