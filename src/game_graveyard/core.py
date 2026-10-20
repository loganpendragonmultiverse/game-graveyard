from __future__ import annotations

import json
import math
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from .history import load_csv, state_as_of, validate_history

REASONS = {"technical", "difficulty", "time", "design", "accessibility", "story", "other"}


def _date(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be an ISO date")
    try:
        parsed = date.fromisoformat(value)
        if parsed.isoformat() != value:
            raise ValueError("dates must use YYYY-MM-DD")
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO date") from exc
    return value


def _playtime_hours(value: Any, game_id: str) -> float:
    message = f"game {game_id} playtime_hours must be finite and non-negative"
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value > sys.float_info.max:
        raise ValueError(message)
    try:
        hours = float(value)
    except OverflowError as exc:
        raise ValueError(message) from exc
    if not math.isfinite(hours) or hours < 0:
        raise ValueError(message)
    return hours


def load_graveyard(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    data = load_csv(text) if path.suffix.lower() == ".csv" else json.loads(text)
    if (
        isinstance(data, dict)
        and isinstance(data.get("games"), list)
        and ("version" not in data or data.get("format") == "game-graveyard-backlog")
    ):
        if "version" in data and data["version"] != 1:
            raise ValueError("backlog import requires version 1")
        if not all(
            isinstance(g, dict) and isinstance(g.get("graveyard_record"), dict)
            for g in data["games"]
        ):
            raise ValueError(
                "Backlog import requires authored graveyard_record metadata; reasons are never inferred"
            )
        data = {"version": 1, "games": [g["graveyard_record"] for g in data["games"]]}
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("graveyard must be a version 1 object")
    games = data.get("games")
    if not isinstance(games, list):
        raise TypeError("games must be a list")
    seen: set[str] = set()
    for game in games:
        if not isinstance(game, dict):
            raise TypeError("each game must be an object")
        for field in ("id", "title", "platform", "reason"):
            if not isinstance(game.get(field), str) or not game[field].strip():
                raise ValueError(f"each game requires non-empty text field: {field}")
        if game["id"] in seen:
            raise ValueError(f"duplicate game id: {game['id']}")
        seen.add(game["id"])
        if game.get("reason_category") not in REASONS:
            raise ValueError(f"game {game['id']} has an invalid reason category")
        _date(game.get("abandoned_on"), "abandoned_on")
        if "reconsider_on" in game:
            _date(game["reconsider_on"], "reconsider_on")
        attempts = game.get("attempts", 1)
        hours = game.get("playtime_hours", 0)
        if not isinstance(attempts, int) or isinstance(attempts, bool) or attempts < 1:
            raise ValueError(f"game {game['id']} attempts must be a positive integer")
        _playtime_hours(hours, game["id"])
        validate_history(game)
    return data


def _is_due(game: dict[str, Any], as_of: str | None) -> bool:
    return bool(
        as_of is not None
        and game.get("reconsider_on")
        and game["reconsider_on"] <= as_of
        and state_as_of(game, as_of) in {"abandoned", "reconsidering"}
    )


def build_report(
    data: dict[str, Any],
    reason: str | None = None,
    as_of: str | None = None,
    *,
    state: str | None = None,
    due_only: bool = False,
) -> dict[str, Any]:
    if as_of is not None:
        _date(as_of, "as_of")
    if reason is not None and reason not in REASONS:
        raise ValueError(f"unknown reason category: {reason}")
    if state is not None and state not in {
        "abandoned",
        "reconsidering",
        "returned",
        "not_yet_abandoned",
    }:
        raise ValueError("unknown decision state")
    if due_only and as_of is None:
        raise ValueError("--due-only requires --as-of")
    games = [
        game
        for game in data["games"]
        if (reason is None or game["reason_category"] == reason)
        and (state is None or state_as_of(game, as_of) == state)
        and (not due_only or _is_due(game, as_of))
    ]
    reason_counts = Counter(game["reason_category"] for game in games)
    platform_counts = Counter(game["platform"] for game in games)
    reconsiderations = [game for game in games if game.get("reconsider_on")]
    total_playtime = sum(
        _playtime_hours(game.get("playtime_hours", 0), game["id"]) for game in games
    )
    if not math.isfinite(total_playtime):
        raise ValueError(
            "total playtime_hours must be finite; use smaller playtimes or a report filter"
        )
    return {
        "version": 1,
        "game_count": len(games),
        "total_playtime_hours": round(total_playtime, 2),
        "reason_counts": dict(sorted(reason_counts.items())),
        "platform_counts": dict(sorted(platform_counts.items())),
        "reconsideration_count": len(reconsiderations),
        "games": games,
        "as_of": as_of,
        "current_states": {g["id"]: state_as_of(g, as_of) for g in games},
        "due_for_reconsideration": [g["id"] for g in games if _is_due(g, as_of)],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Game Graveyard",
        "",
        f"Games: **{report['game_count']}** · Recorded playtime: **{report['total_playtime_hours']} hours** · Reconsiderations: **{report['reconsideration_count']}**",
        "",
    ]
    if report.get("as_of"):
        lines.extend(
            [
                f"As of: {report['as_of']}",
                "Due for reconsideration: " + ", ".join(report["due_for_reconsideration"]),
                "",
            ]
        )
    for game in report["games"]:
        lines.extend(
            [
                f"## {game['title']}",
                "",
                f"- Platform: {game['platform']}",
                f"- Decision state: {report['current_states'][game['id']]}",
                f"- Abandoned: {game['abandoned_on']}",
                f"- Reason: {game['reason_category']} — {game['reason']}",
                f"- Attempts: {game.get('attempts', 1)}",
                f"- Approximate playtime: {game.get('playtime_hours', 0)} hours",
            ]
        )
        if game.get("reconsider_on"):
            lines.append(f"- Reconsider on: {game['reconsider_on']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
