import copy
import json

import pytest

from game_graveyard.cli import main
from game_graveyard.core import build_report
from game_graveyard.sharing import shared_csv, shared_markdown, shared_report


def data():
    return {
        "version": 1,
        "games": [
            {
                "id": "PRIVATE-ID",
                "title": "=Title",
                "platform": "PC",
                "reason": "PRIVATE-REASON",
                "reason_category": "time",
                "abandoned_on": "2026-01-01",
                "reconsider_on": "2026-02-01",
                "playtime_hours": 42,
                "unknown": {"secret": "PRIVATE-EXTRA"},
                "history": [{"state": "returned", "date": "2026-01-02", "note": "PRIVATE-NOTE"}],
            }
        ],
    }


def test_allowlist_without_mutation():
    source = data()
    before = copy.deepcopy(source)
    report = shared_report(build_report(source))
    assert set(report["games"][0]) == {"title", "platform", "reason_category", "state"}
    assert report["games"][0]["state"] == "returned"
    assert source == before
    for output in [json.dumps(report), shared_csv(report), shared_markdown(report)]:
        assert "PRIVATE-" not in output
        assert "2026-" not in output
    assert "'=Title" in shared_csv(report)


@pytest.mark.parametrize("fmt", ["json", "markdown", "csv"])
def test_cli_sharing_all_formats(tmp_path, capsys, fmt):
    path = tmp_path / "private.json"
    path.write_text(json.dumps(data()))
    before = path.read_bytes()
    assert main([str(path), "--share-safe", "--format", fmt]) == 0
    assert "PRIVATE-" not in capsys.readouterr().out
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "extra",
    [["--format", "backlog"], ["--format", "csv", "--csv-lossless"], ["--decision", "returned"]],
)
def test_incompatible_sharing_writes(tmp_path, capsys, extra):
    path = tmp_path / "private.json"
    path.write_text(json.dumps(data()))
    assert main([str(path), "--share-safe", *extra]) == 2
    assert "--share-safe" in capsys.readouterr().err
