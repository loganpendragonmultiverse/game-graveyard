# Changelog

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
