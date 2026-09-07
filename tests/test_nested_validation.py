import json

import pytest

from reading_resume_card_generator.cli import main
from reading_resume_card_generator.core import analyze
from reading_resume_card_generator.preview import render_html


@pytest.mark.parametrize(
    "patch",
    [
        {"work": []},
        {"through": True},
        {"previous_checkpoint": True},
        {"events": [{"milestone": True}]},
        {"events": [{"importance": {}}]},
        {"events": [{"text": 42}]},
        {"threads": [{"text": "x", "status": []}]},
        {"next_step": []},
        {"events": {}},
    ],
)
def test_bad_shapes_return_clean_cli_error(tmp_path, capsys, patch) -> None:
    source = tmp_path / "input.json"
    source.write_text(json.dumps({"work": "A", "through": 1, **patch}))
    assert main([str(source)]) == 2
    assert "Traceback" not in capsys.readouterr().err


def test_card_has_hidden_counts_without_hidden_text(tmp_path, capsys) -> None:
    data = {
        "work": "A",
        "through": 1,
        "events": [
            {"milestone": 1, "text": "Visible", "extra": "HIDDEN"},
            {"milestone": 2, "text": "HIDDEN"},
        ],
    }
    report = analyze(data)
    assert report["still_hidden"]["events"] == 1
    assert "HIDDEN" not in render_html(report)
    source = tmp_path / "input.json"
    source.write_text(json.dumps(data))
    assert main([str(source), "--format", "html"]) == 0
    assert "HIDDEN" not in capsys.readouterr().out
