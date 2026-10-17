import json
from pathlib import Path

from game_graveyard.cli import main
from game_graveyard.core import build_report


def data() -> dict:
    return {
        "version": 1,
        "games": [
            {
                "id": "future",
                "title": "Future",
                "platform": "PC",
                "reason": "Time",
                "reason_category": "time",
                "abandoned_on": "2026-12-01",
                "reconsider_on": "2026-10-01",
            }
        ],
    }


def test_reconsideration_waits_until_abandonment() -> None:
    record = data()
    early = build_report(record, as_of="2026-10-17")
    assert early["current_states"] == {"future": "not_yet_abandoned"}
    assert early["due_for_reconsideration"] == []
    assert build_report(record, as_of="2026-12-01")["due_for_reconsideration"] == ["future"]
    record["games"][0]["history"] = [
        {"date": "2026-12-02", "state": "returned", "note": "Trying again"},
        {"date": "2026-12-03", "state": "reconsidering", "note": "Review again"},
    ]
    assert build_report(record, as_of="2026-12-02")["due_for_reconsideration"] == []
    assert build_report(record, as_of="2026-12-03")["due_for_reconsideration"] == ["future"]


def test_future_abandonment_cli_is_not_due(tmp_path: Path) -> None:
    source = tmp_path / "games.json"
    source.write_text(json.dumps(data()), encoding="utf-8")
    original = source.read_bytes()
    output = tmp_path / "report.json"
    assert (
        main([str(source), "--as-of", "2026-10-17", "--format", "json", "--output", str(output)])
        == 0
    )
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["current_states"]["future"] == "not_yet_abandoned"
    assert report["due_for_reconsideration"] == []
    assert source.read_bytes() == original
