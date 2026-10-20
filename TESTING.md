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

## 1.3.0 regression acceptance

An as-of report no longer lists a game for reconsideration before its abandonment date. Only abandoned or reconsidering games can be due; returned and not-yet-abandoned states are excluded. Authored dates and decision history remain unchanged.

Run the new source and CLI regression cases with the complete existing quality gates. Recheck installed tag-built artifacts after review and release approval.

## 1.3.0 report controls

Use `--state abandoned|reconsidering|returned|not_yet_abandoned` to select the evaluated decision state. Use `--due-only --as-of YYYY-MM-DD` to select games due on a specific date. Filters combine with `--reason` and apply to report counts and all export formats, including sharing copies. Decision files retain the full record set; filters only select the report.

## 1.3.1 numeric boundaries

Reject actual JSON integers `10**400` and `-(10**400)` with actionable finite-number errors. Cover NaN/infinity, booleans, numeric strings, negative/zero boundaries, the maximum finite float and aggregate overflow. Verify CLI failures leave inputs unchanged and create no output or companion file. Keep the full quality, dependency audit, protected PR/main/tag and original installed wheel/source-distribution gates. Do not clamp values or alter ordinary seeded selection.
