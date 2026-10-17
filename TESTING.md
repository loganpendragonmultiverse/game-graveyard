# Testing

Run `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build`. CI also audits dependencies and runs the supported OS/Python matrix.

## 1.1.0 regression acceptance

Run the complete existing suite plus the new regression fixtures. Confirm the documented command produces the selected output, malformed input remains actionable, and source files remain unchanged. Add reversible dated decisions, explicit reconsideration views and local CSV/backlog interchange while preserving original abandonment reasons.

## 1.1.1 acceptance

Repair randomizer interchange and make CSV exports safe for spreadsheet viewing by default.

Verify Include the required version 1 schema marker in backlog exports; Neutralize formula-leading CSV text, including whitespace/control prefixes; Offer explicit lossless CSV export for trusted interchange without silently claiming spreadsheet safety. Run the full existing quality and build gates; release only through protected PR checks and verified tag artifacts.

CSV rejects NUL characters consistently across supported Python versions; use JSON to retain those records. Ordinary whitespace/control prefixes before formula-like text are neutralized in spreadsheet-safe exports.

## 1.2.0 acceptance

Make a sharing copy without private reasons, notes or decision history.

Verify Add --share-safe JSON, Markdown and spreadsheet-safe CSV reports; Exclude IDs, free-text reasons, dates, playtime, history and unknown metadata through an allowlist; Reject sharing mode with decision writes, backlog export or lossless CSV. Run the full existing quality and build gates; release only through protected PR checks and verified tag artifacts.

## 1.2.2 acceptance

Recover cleanly when writing a report and its companion file fails.

Verify Stage every file before reserving new output names and never overwrite existing destinations; Roll back only unchanged files created by the failed command, preserving concurrent changes; Keep stdout delivery inside the output operation and test permission failures, collisions and retry. Run the full existing quality and build gates; release only through protected PR checks and verified tag artifacts.
