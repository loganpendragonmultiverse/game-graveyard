from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

REASONS = {"technical", "difficulty", "time", "design", "accessibility", "story", "other"}


def _date(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be an ISO date")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO date") from exc
    return value


def load_graveyard(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
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
        if not isinstance(hours, (int, float)) or isinstance(hours, bool) or hours < 0:
            raise ValueError(f"game {game['id']} playtime_hours must be non-negative")
    return data


def build_report(data: dict[str, Any], reason: str | None = None) -> dict[str, Any]:
    if reason is not None and reason not in REASONS:
        raise ValueError(f"unknown reason category: {reason}")
    games = [game for game in data["games"] if reason is None or game["reason_category"] == reason]
    reason_counts = Counter(game["reason_category"] for game in games)
    platform_counts = Counter(game["platform"] for game in games)
    reconsiderations = [game for game in games if game.get("reconsider_on")]
    return {
        "version": 1,
        "game_count": len(games),
        "total_playtime_hours": round(
            sum(float(game.get("playtime_hours", 0)) for game in games), 2
        ),
        "reason_counts": dict(sorted(reason_counts.items())),
        "platform_counts": dict(sorted(platform_counts.items())),
        "reconsideration_count": len(reconsiderations),
        "games": games,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Game Graveyard",
        "",
        f"Games: **{report['game_count']}** · Recorded playtime: **{report['total_playtime_hours']} hours** · Reconsiderations: **{report['reconsideration_count']}**",
        "",
    ]
    for game in report["games"]:
        lines.extend(
            [
                f"## {game['title']}",
                "",
                f"- Platform: {game['platform']}",
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
