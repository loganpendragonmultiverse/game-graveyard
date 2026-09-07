from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import REASONS, build_report, load_graveyard, render_markdown
from .history import STATES, decide, export_backlog, export_csv


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report an intentional game graveyard.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--reason", choices=sorted(REASONS))
    parser.add_argument(
        "--format", choices=("markdown", "json", "csv", "backlog"), default="markdown"
    )
    parser.add_argument("--as-of")
    parser.add_argument("--decision", choices=sorted(STATES))
    parser.add_argument("--undo-last", action="store_true")
    parser.add_argument("--game-id")
    parser.add_argument("--date")
    parser.add_argument("--decision-note")
    parser.add_argument("--decision-output", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        data = load_graveyard(args.input)
        if args.decision and args.undo_last:
            raise ValueError("Choose a decision or undo-last")
        if args.decision or args.undo_last:
            if not all((args.game_id, args.date, args.decision_note, args.decision_output)):
                raise ValueError(
                    "Decisions require game-id, date, decision-note and a new decision-output"
                )
            data = decide(
                data,
                args.game_id,
                args.decision,
                args.date,
                args.decision_note,
                undo=args.undo_last,
            )
        elif any((args.game_id, args.date, args.decision_note, args.decision_output)):
            raise ValueError("Decision options require --decision or --undo-last")
        targets = [p for p in (args.output, args.decision_output) if p]
        if len({p.resolve() for p in targets}) != len(targets) or any(p.exists() for p in targets):
            raise ValueError("Outputs must be distinct new files")
        report = build_report(data, args.reason, args.as_of)
        rendered = (
            json.dumps(report, indent=2, ensure_ascii=False) + "\n"
            if args.format == "json"
            else render_markdown(report)
        )
        if args.format == "csv":
            rendered = export_csv(report["games"])
        elif args.format == "backlog":
            rendered = json.dumps(export_backlog(report["games"]), indent=2) + "\n"
        if args.decision_output:
            args.decision_output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        if args.output:
            if args.output.exists():
                raise ValueError(f"output already exists: {args.output}")
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0
