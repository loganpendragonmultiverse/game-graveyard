# Development

Use src and the regression suite. Protected CI must pass before release.

## 1.1.0 improvement session

Add reversible dated decisions, explicit reconsideration views and local CSV/backlog interchange while preserving original abandonment reasons.

Use --decision abandoned|reconsidering|returned with --game-id, --date, --decision-note and --decision-output new.json. --undo-last appends a reversal instead of deleting history. Dates must remain ordered and original abandonment reasons are preserved. --as-of evaluates decision state and due reconsideration dates without scheduling reminders. CSV input/output carries documented fields and JSON history; unsupported extra columns are rejected. --format backlog creates a randomizer-compatible JSON with original graveyard_record metadata for re-import. Ownership is unknown and defaults false, so review backlog rules before drawing. Generic backlog records without authored abandonment metadata are rejected. No storefront login or notification is performed.

Local formatting, lint, strict types and regression tests pass. Public release completion requires the protected CI/CodeQL matrix, tagged artifacts and matching Forge catalog/detail deployment.

## 1.1.1 acceptance

Repair randomizer interchange and make CSV exports safe for spreadsheet viewing by default.

Use `game-graveyard graveyard.json --format backlog --output backlog.json` for a version 1 randomizer input. Ownership still defaults false and must be reviewed. CSV export prefixes formula-like text with an apostrophe by default; this changes those cells intentionally for spreadsheet viewing. `--format csv --csv-lossless` preserves exact cell text for trusted round trips and may contain executable spreadsheet formulas. Neither mode promises that an arbitrary spreadsheet program is safe; inspect exports before opening them.

## 1.2.0 acceptance

Make a sharing copy without private reasons, notes or decision history.

Use game-graveyard graveyard.json --share-safe --format json --output share.json. Sharing copies contain only title, platform, broad reason category and current state. Review those fields too: a title or broad category may still be personal. Private source data stays unchanged. Sharing reports are clearly marked and cannot be used as a lossless backup or re-import file.

## 1.2.2 acceptance

Recover cleanly when writing a report and its companion file fails.

Report and ledger/decision/history files are prepared together. If an ordinary write fails, the command removes only unchanged files it created, so you can fix the destination and retry. Existing files, source inputs and files changed by another process are preserved. Outputs are UTF-8 with LF endings. This handles ordinary write failures; it does not promise a multi-file transaction through power loss or recall text already read from stdout.

## Gold Star review — October 17, 2026

Reviewed release: v1.2.2. Keep a record of games you stopped playing, revisit your decisions and make a sharing copy without private reasons or notes.

Logan considers this project complete. Continue fixes and maintenance, and consider good new ideas. The catalog records the reviewed release.

Definition: https://www.loganpendragonforge.com/open-source/?gold=1
