import csv
import io
import json
from pathlib import Path

import pytest

from game_graveyard.cli import main
from game_graveyard.history import export_backlog, export_csv, load_csv


@pytest.mark.parametrize(
    "text", ["=1+1", "+SUM(A1)", "-2+3", "@SUM(1,2)", " \t=1+1", "\r\n@SUM(A1)", "\v=1+1"]
)
def test_formula_prefixes_neutralized_and_explicit_lossless_preserves(text):
    safe = next(csv.DictReader(io.StringIO(export_csv([{"id": "g", "title": text}]))))
    assert safe["title"] == "'" + text
    original = next(
        csv.DictReader(
            io.StringIO(export_csv([{"id": "g", "title": text}], spreadsheet_safe=False))
        )
    )
    assert original["title"] == text


def test_backlog_has_required_schema_and_preserves_original():
    game = {"id": "g", "title": "Ω", "platform": "PC", "reason": "Private"}
    result = export_backlog([game])
    assert result["version"] == 1
    assert result["games"][0]["graveyard_record"] == game
    assert not result["games"][0]["owned"]


def test_lossless_flag_requires_csv(tmp_path: Path):
    path = tmp_path / "sample.json"
    path.write_text(json.dumps({"version": 1, "games": []}))
    assert main([str(path), "--csv-lossless"]) == 2


def test_nul_csv_rejected_consistently_for_supported_python_versions():
    for safe in (True, False):
        with pytest.raises(ValueError, match="NUL.*JSON"):
            export_csv([{"id": "g", "title": "\0=1+1"}], spreadsheet_safe=safe)
    with pytest.raises(ValueError, match="NUL.*JSON"):
        load_csv("id,title\ng,\0=1+1\n")
