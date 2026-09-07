import json
from pathlib import Path

import pytest

from game_graveyard.cli import main
from game_graveyard.core import build_report, load_graveyard
from game_graveyard.history import decide, export_backlog, export_csv, state_as_of, validate_history


def sample() -> dict:
    return {
        "version": 1,
        "games": [
            {
                "id": "a",
                "title": "Fictional",
                "platform": "PC",
                "reason": "Original reason",
                "reason_category": "time",
                "abandoned_on": "2026-01-01",
                "reconsider_on": "2026-09-01",
                "attempts": 1,
                "playtime_hours": 2.5,
            }
        ],
    }


def test_decision_reversal_preserves_original_and_as_of() -> None:
    original = sample()
    returned = decide(original, "a", "returned", "2026-09-07", "Try again")
    reversed_ = decide(returned, "a", None, "2026-09-08", "Reverse last choice", undo=True)
    assert "history" not in original["games"][0]
    assert reversed_["games"][0]["reason"] == "Original reason"
    assert len(reversed_["games"][0]["history"]) == 2
    assert state_as_of(reversed_["games"][0], "2026-09-07") == "returned"
    assert state_as_of(reversed_["games"][0], "2025-01-01") == "not_yet_abandoned"
    assert build_report(reversed_, as_of="2026-09-08")["due_for_reconsideration"] == ["a"]
    assert build_report(returned, as_of="2026-09-07")["due_for_reconsideration"] == []


def test_interchange_and_decision_cli(tmp_path: Path) -> None:
    source = tmp_path / "graveyard.csv"
    source.write_text(export_csv(sample()["games"]), encoding="utf-8")
    assert load_graveyard(source)["games"][0]["playtime_hours"] == 2.5
    backlog = tmp_path / "backlog.json"
    backlog.write_text(json.dumps(export_backlog(sample()["games"])), encoding="utf-8")
    assert load_graveyard(backlog) == sample()
    output = tmp_path / "decision.json"
    assert (
        main(
            [
                str(source),
                "--game-id",
                "a",
                "--decision",
                "reconsidering",
                "--date",
                "2026-09-07",
                "--decision-note",
                "Review",
                "--decision-output",
                str(output),
                "--as-of",
                "2026-09-07",
            ]
        )
        == 0
    )
    assert load_graveyard(output)["games"][0]["history"][0]["state"] == "reconsidering"
    assert main([str(source), "--decision", "returned"]) == 2
    assert main([str(source), "--game-id", "a"]) == 2
    assert main([str(source), "--decision", "returned", "--undo-last"]) == 2
    for fmt in ("csv", "backlog"):
        assert main([str(output), "--format", fmt]) == 0
    assert main([str(output), "--output", str(output)]) == 2


@pytest.mark.parametrize(
    "history", [None, [None], [{"state": "returned", "date": "2025-01-01", "note": "x"}]]
)
def test_invalid_history(history: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        validate_history({**sample()["games"][0], "history": history})


def test_invalid_decisions_and_csv(tmp_path: Path) -> None:
    for identifier, state, when, note, undo in [
        ("missing", "returned", "2026-09-07", "x", False),
        ("a", None, "2026-09-07", "x", True),
        ("a", "invalid", "2026-09-07", "", False),
    ]:
        with pytest.raises(ValueError):
            decide(sample(), identifier, state, when, note, undo=undo)
    source = tmp_path / "bad.csv"
    for text in ("id,id\na,a", "unknown\nx", "id,title\na,b,c"):
        source.write_text(text, encoding="utf-8")
        with pytest.raises(ValueError):
            load_graveyard(source)
    source = tmp_path / "backlog.json"
    source.write_text('{"games":[{"id":"a"}]}', encoding="utf-8")
    with pytest.raises(ValueError, match="authored"):
        load_graveyard(source)
