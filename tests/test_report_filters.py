import json

import pytest

from game_graveyard.cli import main
from game_graveyard.core import build_report


def records():
    return {
        "version": 1,
        "games": [
            {
                "id": name,
                "title": name,
                "platform": "PC",
                "reason": "private",
                "reason_category": "time",
                "abandoned_on": date,
                "reconsider_on": "2026-01-01",
                "history": history,
            }
            for name, date, history in [
                ("due", "2026-01-01", []),
                ("future", "2027-01-01", []),
                (
                    "returned",
                    "2026-01-01",
                    [{"date": "2026-02-01", "state": "returned", "note": "private"}],
                ),
            ]
        ],
    }


def test_filters_use_as_of_state_and_due_dates():
    data = records()
    report = build_report(data, as_of="2026-10-17", due_only=True)
    assert [g["id"] for g in report["games"]] == ["due"]
    assert report["game_count"] == 1
    assert report["due_for_reconsideration"] == ["due"]
    assert build_report(data, as_of="2026-10-17", state="returned", due_only=True)["games"] == []
    assert (
        build_report(data, as_of="2026-10-17", state="not_yet_abandoned")["games"][0]["id"]
        == "future"
    )
    with pytest.raises(ValueError, match="requires --as-of"):
        build_report(data, due_only=True)
    with pytest.raises(ValueError, match="unknown decision"):
        build_report(data, state="invalid")


def test_cli_filters_share_copy_and_preserves_source(tmp_path, capsys):
    path = tmp_path / "games.json"
    path.write_text(json.dumps(records()), encoding="utf-8")
    before = path.read_bytes()
    assert (
        main(
            [
                str(path),
                "--as-of",
                "2026-10-17",
                "--due-only",
                "--state",
                "abandoned",
                "--share-safe",
                "--format",
                "json",
            ]
        )
        == 0
    )
    report = json.loads(capsys.readouterr().out)
    assert report["game_count"] == 1
    assert report["games"][0]["title"] == "due"
    assert "private" not in json.dumps(report)
    assert path.read_bytes() == before
    assert main([str(path), "--due-only"]) == 2
    assert "requires --as-of" in capsys.readouterr().err


@pytest.mark.parametrize("format", ["csv", "backlog"])
def test_filtered_exports_contain_only_selected_games(tmp_path, capsys, format):
    source = tmp_path / "games.json"
    source.write_text(json.dumps(records()), encoding="utf-8")
    assert main([str(source), "--due-only", "--as-of", "2026-10-17", "--format", format]) == 0
    rendered = capsys.readouterr().out
    if format == "backlog":
        assert [game["title"] for game in json.loads(rendered)["games"]] == ["due"]
    else:
        import csv
        import io

        assert [game["title"] for game in csv.DictReader(io.StringIO(rendered))] == ["due"]
