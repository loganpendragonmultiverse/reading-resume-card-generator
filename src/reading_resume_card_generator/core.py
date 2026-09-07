from __future__ import annotations

import json
from typing import Any

PROJECT = "reading-resume-card-generator"
IMPORTANCE = {"low", "medium", "high", "critical"}


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    work = _require(data, "work")
    if not isinstance(work, str) or not work.strip():
        raise ValueError("work must be nonempty text")
    through = _require(data, "through")
    previous = data.get("previous_checkpoint", 0)
    if not isinstance(through, int) or isinstance(through, bool) or through < 0:
        raise ValueError("through must be a non-negative integer")
    if (
        not isinstance(previous, int)
        or isinstance(previous, bool)
        or previous < 0
        or previous > through
    ):
        raise ValueError("previous_checkpoint must be between zero and through")

    def normalized(label: str) -> list[dict[str, Any]]:
        raw = data.get(label, [])
        if not isinstance(raw, list):
            raise TypeError("events, characters, and threads must be lists")
        result = []
        for index, value in enumerate(raw, 1):
            if not isinstance(value, dict):
                raise TypeError(f"{label} item {index} must be an object")
            milestone = value.get("milestone", 0)
            if not isinstance(milestone, int) or isinstance(milestone, bool) or milestone < 0:
                raise ValueError(f"{label} item {index} milestone must be non-negative")
            importance = value.get("importance", "medium")
            if not isinstance(importance, str) or importance not in IMPORTANCE:
                raise ValueError(f"{label} item {index} has invalid importance")
            field = "name" if label == "characters" else "text"
            if not isinstance(value.get(field), str):
                raise ValueError(f"{label} item {index} {field} must be text")
            status = value.get("status", "open")
            if label == "threads" and (
                not isinstance(status, str) or status not in {"open", "resolved"}
            ):
                raise ValueError(f"threads item {index} status must be open or resolved")
            if milestone <= through:
                result.append(
                    {
                        field: value[field],
                        "milestone": milestone,
                        "importance": importance,
                        **({"status": status} if label == "threads" else {}),
                    }
                )
        return result

    events = normalized("events")
    characters = normalized("characters")
    threads = normalized("threads")
    open_threads = [item for item in threads if item.get("status", "open") == "open"]
    resolved_threads = [item for item in threads if item.get("status", "open") == "resolved"]
    invalid = [item for item in threads if item.get("status", "open") not in {"open", "resolved"}]
    if invalid:
        raise ValueError("thread status must be open or resolved")
    if not isinstance(data.get("next_step", ""), str):
        raise ValueError("next_step must be text")
    return {
        "version": 2,
        "project": PROJECT,
        "work": work,
        "through": through,
        "previous_checkpoint": previous,
        "last_events": events[-5:],
        "visible_events": events,
        "still_hidden": {
            label: sum(item.get("milestone", 0) > through for item in data.get(label, []))
            for label in ("events", "characters", "threads")
        },
        "characters": characters,
        "open_threads": open_threads,
        "resolved_threads": resolved_threads,
        "changes_since_previous": {
            "events": [x for x in events if x["milestone"] > previous],
            "characters": [x for x in characters if x["milestone"] > previous],
            "threads": [x for x in threads if x["milestone"] > previous],
        },
        "next_step": data.get("next_step", "Resume at the recorded position."),
    }


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False, default=str) + "\n"


def _items(lines: list[str], title: str, values: list[dict[str, Any]], field: str) -> None:
    lines.extend([f"## {title}", ""])
    if not values:
        lines.append("- None recorded.")
    for item in values:
        lines.append(
            f"- **{item['importance'].title()}** - {item.get(field, item.get('text', ''))} (milestone {item['milestone']})"
        )
    lines.append("")


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# Reading Resume Card Generator: {report['work']}",
        "",
        f"Checkpoint: **{report['through']}**",
        f"Next: {report['next_step']}",
        "",
    ]
    _items(lines, "Recent Events", report["last_events"], "text")
    _items(lines, "Characters", report["characters"], "name")
    _items(lines, "Open Threads", report["open_threads"], "text")
    _items(lines, "Resolved Threads", report["resolved_threads"], "text")
    changes = report["changes_since_previous"]
    lines.extend(
        [
            "## Changes Since Previous Checkpoint",
            "",
            f"- Events: {len(changes['events'])}",
            f"- Characters: {len(changes['characters'])}",
            f"- Threads: {len(changes['threads'])}",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"
