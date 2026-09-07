# Development

Use src and the regression suite. Protected CI must pass before release.

## 1.1.0 improvement session

Add reversible dated decisions, explicit reconsideration views and local CSV/backlog interchange while preserving original abandonment reasons.

Use --decision abandoned|reconsidering|returned with --game-id, --date, --decision-note and --decision-output new.json. --undo-last appends a reversal instead of deleting history. Dates must remain ordered and original abandonment reasons are preserved. --as-of evaluates decision state and due reconsideration dates without scheduling reminders. CSV input/output carries documented fields and JSON history; unsupported extra columns are rejected. --format backlog creates a randomizer-compatible JSON with original graveyard_record metadata for re-import. Ownership is unknown and defaults false, so review backlog rules before drawing. Generic backlog records without authored abandonment metadata are rejected. No storefront login or notification is performed.

Local formatting, lint, strict types and regression tests pass. Public release completion requires the protected CI/CodeQL matrix, tagged artifacts and matching Forge catalog/detail deployment.
