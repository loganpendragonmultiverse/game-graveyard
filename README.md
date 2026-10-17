# Game Graveyard

> ⭐ **Gold Star Project**
> I consider this project complete. Fixes, maintenance and good new ideas are still welcome.
> [About Gold Stars](https://www.loganpendragonforge.com/open-source/?gold=1)
>
> Keep a record of games you stopped playing, revisit your decisions and make a sharing copy without private reasons or notes.

## Current release 1.2.2

Recover cleanly when writing a report and its companion file fails.

Report and ledger/decision/history files are prepared together. If an ordinary write fails, the command removes only unchanged files it created, so you can fix the destination and retry. Existing files, source inputs and files changed by another process are preserved. Outputs are UTF-8 with LF endings. This handles ordinary write failures; it does not promise a multi-file transaction through power loss or recall text already read from stdout.

## Updates in 1.2.1

Make a sharing copy without private reasons, notes or decision history.

Use game-graveyard graveyard.json --share-safe --format json --output share.json. Sharing copies contain only title, platform, broad reason category and current state. Review those fields too: a title or broad category may still be personal. Private source data stays unchanged. Sharing reports are clearly marked and cannot be used as a lossless backup or re-import file.

## Updates in 1.1.1

Repair randomizer interchange and make CSV exports safe for spreadsheet viewing by default.

Use `game-graveyard graveyard.json --format backlog --output backlog.json` for a version 1 randomizer input. Ownership still defaults false and must be reviewed. CSV export prefixes formula-like text with an apostrophe by default; this changes those cells intentionally for spreadsheet viewing. `--format csv --csv-lossless` preserves exact cell text for trusted round trips and may contain executable spreadsheet formulas. Neither mode promises that an arbitrary spreadsheet program is safe; inspect exports before opening them.

[![CI](https://github.com/loganpendragonmultiverse/game-graveyard/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/game-graveyard/actions/workflows/ci.yml)

Game Graveyard keeps intentionally abandoned games out of an active backlog without erasing the decision. A portable JSON record can retain the platform, attempts, approximate playtime, reason category, explanation, abandonment date, and an optional reconsideration date.

## Three-minute start

```bash
python -m pip install .
game-graveyard examples/graveyard.json
game-graveyard examples/graveyard.json --reason technical --format json
```

Reports summarize entries by reason and platform, list scheduled reconsiderations separately, and support Markdown or JSON output. Existing report files are refused.

The tool does not import platform libraries, judge whether a game is good, or calculate playtime. The owner supplies every record and can choose deliberately broad notes for privacy. Requires Python 3.10 or newer.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).

## Version 1.1.0: reviewed improvements

Add reversible dated decisions, explicit reconsideration views and local CSV/backlog interchange while preserving original abandonment reasons.

```bash
game-graveyard examples/graveyard.json --as-of 2026-09-07 --format json
```

Use --decision abandoned|reconsidering|returned with --game-id, --date, --decision-note and --decision-output new.json. --undo-last appends a reversal instead of deleting history. Dates must remain ordered and original abandonment reasons are preserved. --as-of evaluates decision state and due reconsideration dates without scheduling reminders. CSV input/output carries documented fields and JSON history; unsupported extra columns are rejected. --format backlog creates a randomizer-compatible JSON with original graveyard_record metadata for re-import. Ownership is unknown and defaults false, so review backlog rules before drawing. Generic backlog records without authored abandonment metadata are rejected. No storefront login or notification is performed.

CSV rejects NUL characters consistently across supported Python versions; use JSON to retain those records. Ordinary whitespace/control prefixes before formula-like text are neutralized in spreadsheet-safe exports.
