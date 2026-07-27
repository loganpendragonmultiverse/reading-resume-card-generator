import json
from pathlib import Path

import pytest

from reading_resume_card_generator.cli import main
from reading_resume_card_generator.core import PROJECT, analyze, render_json, render_markdown


def test_representative_sample_has_expected_result():
    data = json.loads(
        (Path(__file__).parents[1] / "examples" / "sample.json").read_text(encoding="utf-8")
    )
    report = analyze(data)
    assert report["version"] == 2 and report["project"] == PROJECT
    assert len(report["last_events"]) == 1 and len(report["characters"]) == 1
    assert "Recent Events" in render_markdown(report)
    assert f'"project": "{PROJECT}"' in render_json(report)
    assert PROJECT.replace("-", " ").title() in render_markdown(report)


def test_missing_required_input_is_rejected():
    with pytest.raises(ValueError):
        analyze({})


def test_threads_changes_and_validation():
    data = {
        "work": "Harbor",
        "through": 4,
        "previous_checkpoint": 2,
        "events": [{"milestone": 3, "text": "Returned", "importance": "high"}],
        "characters": [],
        "threads": [
            {"milestone": 1, "text": "Old", "status": "resolved"},
            {"milestone": 4, "text": "New", "status": "open", "importance": "critical"},
        ],
    }
    report = analyze(data)
    assert len(report["open_threads"]) == 1 and len(report["resolved_threads"]) == 1
    assert len(report["changes_since_previous"]["threads"]) == 1
    with pytest.raises(ValueError, match="previous_checkpoint"):
        analyze({"work": "A", "through": 1, "previous_checkpoint": 2})
    with pytest.raises(ValueError, match="importance"):
        analyze({"work": "A", "through": 1, "events": [{"milestone": 1, "importance": "huge"}]})
    with pytest.raises(TypeError, match="must be lists"):
        analyze({"work": "A", "through": 1, "events": {}})
    with pytest.raises(TypeError, match="must be an object"):
        analyze({"work": "A", "through": 1, "events": ["bad"]})


def test_cli_json_and_output_safety(tmp_path, capsys):
    source = Path(__file__).parents[1] / "examples" / "sample.json"
    assert main([str(source), "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["project"] == PROJECT
    output = tmp_path / "report.md"
    output.write_text("keep", encoding="utf-8")
    assert main([str(source), "--output", str(output)]) == 2
