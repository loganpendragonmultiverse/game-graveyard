# Changelog

## 1.3.1 - 2026-10-20

- Include handoff documentation and runnable examples in wheels and source distributions.

- Return controlled input errors for integers outside the finite float range instead of raising OverflowError.
- Validate individual numeric values before report calculations; preserve supported finite values and original input files.
- Reject a non-finite report playtime total before rendering or creating report/decision files.

## 1.3.0 - 2026-10-17

- Add `--state` and `--due-only --as-of YYYY-MM-DD` report filters. Counts and exports reflect the selection; decision files retain all records.
- An as-of report no longer lists a game for reconsideration before its abandonment date. Only abandoned or reconsidering games can be due; returned and not-yet-abandoned states are excluded. Authored dates and decision history remain unchanged.

## 1.2.2 - 2026-10-17

- Require YYYY-MM-DD dates so as-of comparisons cannot misorder compact or week-date spellings.

- Stage every file before reserving new output names and never overwrite existing destinations
- Roll back only unchanged files created by the failed command, preserving concurrent changes
- Keep stdout delivery inside the output operation and test permission failures, collisions and retry

## 1.2.1 - 2026-10-17

- Reject NUL characters in sharing CSV, matching ordinary CSV behavior; JSON still preserves those labels.

## 1.2.0 - 2026-10-17

- Add --share-safe JSON, Markdown and spreadsheet-safe CSV reports
- Exclude IDs, free-text reasons, dates, playtime, history and unknown metadata through an allowlist
- Reject sharing mode with decision writes, backlog export or lossless CSV

## 1.1.1 - 2026-10-17

- Include the required version 1 schema marker in backlog exports
- Neutralize formula-leading CSV text, including whitespace/control prefixes
- Offer explicit lossless CSV export for trusted interchange without silently claiming spreadsheet safety

## 1.1.0 - 2026-09-07

- Add reversible dated decisions, explicit reconsideration views and local CSV/backlog interchange while preserving original abandonment reasons.
- Added regression coverage for the audited behavior and invalid inputs.

## 1.0.0 - 2026-07-26

- Added validated abandoned-game records and reason categories.
- Added reason filtering, reconsideration visibility, and aggregate summaries.
- Added Markdown and JSON reports with safe output handling.

CSV rejects NUL characters consistently across supported Python versions; use JSON to retain those records. Ordinary whitespace/control prefixes before formula-like text are neutralized in spreadsheet-safe exports.
