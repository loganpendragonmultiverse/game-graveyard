# Game Graveyard

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
