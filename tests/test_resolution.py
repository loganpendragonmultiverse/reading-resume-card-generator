import copy
import json
import re

import pytest

from reading_resume_card_generator.core import analyze, render_json, render_markdown
from reading_resume_card_generator.preview import render_html


def source(through=5, previous=1):
    return {
        "work": "Synthetic book",
        "through": through,
        "previous_checkpoint": previous,
        "threads": [
            {
                "text": "Who sent the letter?",
                "milestone": 2,
                "status": "resolved",
                "resolution_milestone": 5,
                "resolution_text": "SPOILER_CANARY",
            },
            {"text": "FUTURE_CANARY", "milestone": 9},
        ],
    }


@pytest.mark.parametrize("through,resolved,delta", [(4, False, 0), (5, True, 1), (6, True, 1)])
def test_boundaries_and_deltas(through, resolved, delta):
    data = source(through, 3)
    original = copy.deepcopy(data)
    report = analyze(data)
    assert bool(report["resolved_threads"]) is resolved
    assert len(report["changes_since_previous"]["threads"]) == delta
    assert data == original
    item = (report["resolved_threads"] or report["open_threads"])[0]
    assert ("resolution_milestone" in item) is resolved
    for render in (render_json, render_markdown, render_html):
        output = render(report)
        assert "SPOILER_CANARY" not in output
        assert "FUTURE_CANARY" not in output


@pytest.mark.parametrize("value", [None, True, -1, 1, 2.5, "5"])
def test_invalid_resolution(value):
    data = source()
    data["threads"][0]["resolution_milestone"] = value
    with pytest.raises(ValueError, match="resolution_milestone"):
        analyze(data)


def test_unknown_status_and_future_invalid_chronology():
    data = source(1, 0)
    data["threads"][0]["status"] = "open"
    with pytest.raises(ValueError, match="resolution_milestone"):
        analyze(data)
    data["threads"][0]["status"] = "unknown"
    with pytest.raises(ValueError, match="status"):
        analyze(data)


def test_equal_milestone_and_legacy_parity():
    data = source(2, 0)
    data["threads"][0]["resolution_milestone"] = 2
    assert len(analyze(data)["resolved_threads"]) == 1
    del data["threads"][0]["resolution_milestone"]
    assert analyze(data)["resolved_threads"][0] == {
        "text": "Who sent the letter?",
        "milestone": 2,
        "importance": "medium",
        "status": "resolved",
    }
    data = source(6, 5)
    assert analyze(data)["changes_since_previous"]["threads"] == []


def test_export_ceiling():
    output = render_html(analyze(source(4)))
    payload = json.loads(re.search(r'id="data">(.*?)</script>', output, re.DOTALL)[1])
    assert payload["through"] == 4
    assert "resolution_milestone" not in json.dumps(payload)
    assert payload["open_threads"][0]["status"] == "open"
