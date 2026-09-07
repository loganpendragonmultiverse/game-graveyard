"""Reversible local decisions and lossless graveyard CSV/backlog interchange."""

from __future__ import annotations

import copy
import csv
import io
import json
from datetime import date
from typing import Any

STATES = {"abandoned", "reconsidering", "returned"}
FIELDS = (
    "id",
    "title",
    "platform",
    "reason",
    "reason_category",
    "abandoned_on",
    "reconsider_on",
    "attempts",
    "playtime_hours",
    "history",
)


def validate_history(game: dict[str, Any]) -> None:
    history = game.get("history", [])
    if not isinstance(history, list):
        raise TypeError("history must be an array")
    last = date.fromisoformat(game["abandoned_on"])
    for index, event in enumerate(history):
        if (
            not isinstance(event, dict)
            or event.get("state") not in STATES
            or not isinstance(event.get("note"), str)
            or not isinstance(event.get("date"), str)
        ):
            raise ValueError(f"history[{index}] requires state, date and note")
        current = date.fromisoformat(event["date"])
        if current < last:
            raise ValueError("history dates must be ordered after abandonment")
        last = current


def decide(
    data: dict[str, Any],
    identifier: str,
    state: str | None,
    when: str,
    note: str,
    *,
    undo: bool = False,
) -> dict[str, Any]:
    result = copy.deepcopy(data)
    matches = [g for g in result["games"] if g["id"] == identifier]
    if len(matches) != 1:
        raise ValueError("decision requires one known game ID")
    game = matches[0]
    history = game.setdefault("history", [])
    if undo:
        if not history:
            raise ValueError("there is no decision to reverse")
        state = history[-2]["state"] if len(history) > 1 else "abandoned"
    if state not in STATES or not note.strip():
        raise ValueError("decision requires a known state and a non-empty note")
    history.append(
        {
            "state": state,
            "date": when,
            "note": note,
            "reverses_event": len(history) - 1 if undo else None,
        }
    )
    validate_history(game)
    return result


def state_as_of(game: dict[str, Any], as_of: str | None) -> str:
    if as_of is not None and as_of < game["abandoned_on"]:
        return "not_yet_abandoned"
    history = game.get("history", [])
    eligible = [e for e in history if as_of is None or e["date"] <= as_of]
    return eligible[-1]["state"] if eligible else "abandoned"


def load_csv(text: str) -> dict[str, Any]:
    reader = csv.DictReader(io.StringIO(text.lstrip("\ufeff")))
    headers = reader.fieldnames or []
    if len(headers) != len(set(headers)) or set(headers) - set(FIELDS):
        raise ValueError("CSV has duplicate or unsupported headers")
    games = []
    for row in reader:
        if None in row or any(v is None for v in row.values()):
            raise ValueError("CSV row width must match headers")
        record: dict[str, Any] = {k: v for k, v in row.items() if v != ""}
        if "attempts" in record:
            record["attempts"] = int(record["attempts"])
        if "playtime_hours" in record:
            record["playtime_hours"] = float(record["playtime_hours"])
        if "history" in record:
            record["history"] = json.loads(record["history"])
        games.append(record)
    return {"version": 1, "games": games}


def export_csv(games: list[dict[str, Any]]) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=FIELDS, extrasaction="ignore")
    writer.writeheader()
    for game in games:
        writer.writerow({**game, "history": json.dumps(game.get("history", []))})
    return output.getvalue()


def export_backlog(games: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "games": [
            {
                "id": game["id"],
                "title": game["title"],
                "platform": game["platform"],
                "genres": [],
                "moods": [],
                "owned": False,
                "hours": 0,
                "weight": 1,
                "graveyard_record": game,
            }
            for game in games
        ],
        "interchange_note": "Ownership is unknown and defaults false; review backlog rules before drawing. Original graveyard records support lossless re-import.",
    }
