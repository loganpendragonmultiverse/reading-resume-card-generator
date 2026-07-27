from __future__ import annotations

import json
from typing import Any

PROJECT = "reading-resume-card-generator"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _reading_resume(data: dict[str, Any]) -> dict[str, Any]:
    work = _require(data, "work")
    through = _require(data, "through")
    if not isinstance(through, int) or through < 0:
        raise ValueError("through must be a non-negative integer")

    def visible(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [item for item in items if int(item.get("milestone", 0)) <= through]

    events = data.get("events", [])
    characters = data.get("characters", [])
    threads = data.get("threads", [])
    if not all(isinstance(items, list) for items in (events, characters, threads)):
        raise ValueError("events, characters, and threads must be lists")
    return {
        "work": work,
        "through": through,
        "last_events": visible(events)[-5:],
        "characters": visible(characters),
        "open_threads": visible(threads),
        "next_step": data.get("next_step", "Resume at the recorded position."),
    }


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    return {"version": 1, "project": PROJECT, **_reading_resume(data)}


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False, default=str) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# {report['project'].replace('-', ' ').title()} report", ""]
    for key, value in report.items():
        if key not in {"version", "project"}:
            lines.extend(
                [
                    f"## {key.replace('_', ' ').title()}",
                    "",
                    f"```json\n{json.dumps(value, indent=2, ensure_ascii=False, default=str)}\n```",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"
