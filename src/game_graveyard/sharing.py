"""Build sharing reports from an explicit field allowlist."""

from __future__ import annotations

import csv
import io
from typing import Any

FIELDS = ("title", "platform", "reason_category", "state")


def shared_report(report: dict[str, Any]) -> dict[str, Any]:
    games = [
        {
            "title": g["title"],
            "platform": g["platform"],
            "reason_category": g["reason_category"],
            "state": report["current_states"][g["id"]],
        }
        for g in report["games"]
    ]
    return {
        "version": 1,
        "format": "game-graveyard-share",
        "game_count": len(games),
        "games": games,
        "privacy_note": "Only titles, platforms, broad reason categories and current states are included. Review those fields before sharing. This is not a backup or re-import format.",
    }


def shared_csv(report: dict[str, Any]) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=FIELDS)
    writer.writeheader()
    for g in report["games"]:
        writer.writerow(
            {k: "'" + v if v.lstrip().startswith(("=", "+", "-", "@")) else v for k, v in g.items()}
        )
    return output.getvalue()


def shared_markdown(report: dict[str, Any]) -> str:
    lines = ["# Game Graveyard — sharing copy", "", report["privacy_note"], ""]
    for game in report["games"]:
        # Escape Markdown/HTML so authored labels are plain text rather than links or markup.
        values = [
            str(game[k])
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", " ")
            .replace("\r", " ")
            for k in FIELDS
        ]
        values = ["".join("\\" + c if c in "\\`*_{}[]()#+-.!|" else c for c in v) for v in values]
        lines.append("- " + " · ".join(values))
    return "\n".join(lines) + "\n"
