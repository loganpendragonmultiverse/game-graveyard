import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from game_graveyard.cli import main
from game_graveyard.core import build_report, load_graveyard, render_markdown


def graveyard() -> dict[str, Any]:
    return {
        "version": 1,
        "games": [
            {
                "id": "ridge",
                "title": "Glass Ridge",
                "platform": "PC",
                "abandoned_on": "2026-07-01",
                "reason_category": "technical",
                "reason": "Crashes",
                "attempts": 3,
                "playtime_hours": 4.5,
                "reconsider_on": "2027-01-01",
            },
            {
                "id": "tower",
                "title": "Quiet Tower",
                "platform": "Console",
                "abandoned_on": "2026-06-01",
                "reason_category": "time",
                "reason": "Too long",
            },
        ],
    }


def write(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


def test_report_filter_and_markdown() -> None:
    report = build_report(graveyard())
    assert report["game_count"] == 2
    assert report["total_playtime_hours"] == 4.5
    assert "Reconsider on" in render_markdown(report)
    assert build_report(graveyard(), "technical")["game_count"] == 1
    with pytest.raises(ValueError, match="unknown reason"):
        build_report(graveyard(), "missing")


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (lambda data: data.update(version=2), "version 1"),
        (lambda data: data.update(games="bad"), "games must"),
        (lambda data: data["games"].append("bad"), "must be an object"),
        (lambda data: data["games"][0].update(title=""), "field: title"),
        (lambda data: data["games"].append(data["games"][0].copy()), "duplicate"),
        (lambda data: data["games"][0].update(reason_category="bad"), "invalid reason"),
        (lambda data: data["games"][0].update(abandoned_on="today"), "ISO date"),
        (lambda data: data["games"][0].update(attempts=0), "positive integer"),
        (lambda data: data["games"][0].update(playtime_hours=-1), "non-negative"),
    ],
)
def test_validation(tmp_path: Path, change: Callable[[dict[str, Any]], None], message: str) -> None:
    data = graveyard()
    change(data)
    path = tmp_path / "graveyard.json"
    write(path, data)
    with pytest.raises((TypeError, ValueError), match=message):
        load_graveyard(path)


def test_cli_json_and_safe_output(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "graveyard.json"
    write(path, graveyard())
    assert main([str(path), "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["game_count"] == 2
    output = tmp_path / "report.md"
    assert main([str(path), "--output", str(output)]) == 0
    assert main([str(path), "--output", str(output)]) == 2
