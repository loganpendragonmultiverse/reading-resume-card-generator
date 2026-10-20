import copy
import json

import pytest

from reading_resume_card_generator.cli import main
from reading_resume_card_generator.core import analyze, render_markdown


def test_recent_events_use_milestones_and_stable_ties():
    data = {
        "work": "Example",
        "through": 9,
        "events": [
            {"milestone": point, "text": text}
            for point, text in [
                (9, "latest"),
                (1, "first"),
                (5, "tie-one"),
                (5, "tie-two"),
                (2, "second"),
                (3, "third"),
                (10, "FUTURE"),
            ]
        ],
    }
    before = copy.deepcopy(data)
    report = analyze(data)
    assert [x["text"] for x in report["last_events"]] == [
        "second",
        "third",
        "tie-one",
        "tie-two",
        "latest",
    ]
    assert "FUTURE" not in json.dumps(report)
    assert data == before


def test_dangling_output_does_not_create_target(tmp_path):
    source = tmp_path / "source.json"
    source.write_text(json.dumps({"work": "Example", "through": 0}))
    target, output = tmp_path / "absent", tmp_path / "output"
    try:
        output.symlink_to(target)
    except OSError:
        pytest.skip("symlink unavailable")
    assert main([str(source), "--output", str(output)]) == 2
    assert not target.exists()


def test_markdown_keeps_authored_markup_literal():
    hostile = "<img src=x onerror=alert(1)>\n# Forged\n- [x] done"
    text = render_markdown(
        analyze(
            {"work": hostile, "through": 1, "next_step": hostile, "events": [{"text": hostile}]}
        )
    )
    assert "<img" not in text
    assert "&lt;img" in text
    assert "\n# Forged" not in text
    assert "\n- [x] done" not in text
    assert "\\# Forged" in text
