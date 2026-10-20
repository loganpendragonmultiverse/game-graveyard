import json
import math
import sys
from pathlib import Path
from typing import Any

import pytest

from game_graveyard.cli import main
from game_graveyard.core import build_report, load_graveyard


def graveyard(*hours: float) -> dict[str, Any]:
    return {
        "version": 1,
        "games": [
            {
                "id": str(i),
                "title": "Boundary",
                "platform": "PC",
                "reason": "Time",
                "reason_category": "time",
                "abandoned_on": "2026-01-01",
                "playtime_hours": value,
            }
            for i, value in enumerate(hours)
        ],
    }


@pytest.mark.parametrize(
    "value",
    [
        10**400,
        -(10**400),
        int(sys.float_info.max) + 1,
        float("nan"),
        float("inf"),
        float("-inf"),
        True,
        "2",
        -1,
    ],
)
def test_playtime_rejected_by_loader_and_report(tmp_path: Path, value: Any) -> None:
    data = graveyard(value)
    path = tmp_path / "input.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    before = path.read_bytes()
    with pytest.raises(ValueError, match="playtime_hours must be finite and non-negative"):
        load_graveyard(path)
    with pytest.raises(ValueError, match="playtime_hours must be finite and non-negative"):
        build_report(data)
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "value", [0, -0.0, 1.5, 10**300, sys.float_info.max, int(sys.float_info.max)]
)
def test_supported_playtime_is_not_clamped(tmp_path: Path, value: float) -> None:
    data = graveyard(value)
    path = tmp_path / "input.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    loaded = load_graveyard(path)
    assert loaded["games"][0]["playtime_hours"] == value
    report = build_report(loaded)
    assert math.isfinite(report["total_playtime_hours"])
    assert report["total_playtime_hours"] == round(float(value), 2)


def test_aggregate_overflow_and_filtered_boundary(tmp_path: Path) -> None:
    data = graveyard(sys.float_info.max, sys.float_info.max)
    data["games"][1]["reason_category"] = "technical"
    path = tmp_path / "input.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    loaded = load_graveyard(path)
    with pytest.raises(ValueError, match="total playtime_hours must be finite"):
        build_report(loaded)
    assert build_report(loaded, "time")["total_playtime_hours"] == sys.float_info.max


@pytest.mark.parametrize("hours", [(10**400,), (sys.float_info.max, sys.float_info.max)])
def test_cli_numeric_error_writes_nothing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], hours: tuple[float, ...]
) -> None:
    path = tmp_path / "input.json"
    path.write_text(json.dumps(graveyard(*hours)), encoding="utf-8")
    before = path.read_bytes()
    report = tmp_path / "report.json"
    decision = tmp_path / "decision.json"
    assert (
        main(
            [
                str(path),
                "--format",
                "json",
                "--output",
                str(report),
                "--decision",
                "reconsidering",
                "--game-id",
                "0",
                "--date",
                "2026-10-20",
                "--decision-note",
                "Review",
                "--decision-output",
                str(decision),
            ]
        )
        == 2
    )
    captured = capsys.readouterr()
    assert "finite" in captured.err and "Traceback" not in captured.err
    assert captured.out == ""
    assert path.read_bytes() == before
    assert not report.exists() and not decision.exists()


def test_csv_extreme_playtime_is_a_controlled_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "input.csv"
    path.write_text(
        "id,title,platform,reason,reason_category,abandoned_on,playtime_hours\n"
        + "a,Boundary,PC,Time,time,2026-01-01,"
        + str(10**400)
        + "\n",
        encoding="utf-8",
    )
    before = path.read_bytes()
    output = tmp_path / "report.json"
    assert main([str(path), "--format", "json", "--output", str(output)]) == 2
    captured = capsys.readouterr()
    assert "playtime_hours must be finite" in captured.err and captured.out == ""
    assert path.read_bytes() == before and not output.exists()
