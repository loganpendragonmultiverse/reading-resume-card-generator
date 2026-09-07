# Development contract

Create spoiler-controlled return-to-reading cards for pauses within a book or series.

Preserve deterministic, source-safe behavior and the interpretation boundary documented in the README. Every feature release must update tests, version metadata, changelog, README claims, repository metadata, release assets, and the Forge catalog together.

## 1.2.0 improvement session

Validate nested checkpoint records and add printable pocket/phone cards with checkpoint previews and hidden-item counts.

Work and display fields must be text; milestone/checkpoint fields must be nonnegative integers, excluding booleans. Event, character and thread records are validated before filtering. HTML supports phone and pocket-print layouts and earlier checkpoint previews, with counts of newly included and still-hidden items. Future text and unsupported extra fields are excluded from the export; only hidden-item counts remain. To advance beyond the exported ceiling, update the private input's through checkpoint and regenerate. The page does not modify the original input.

Local formatting, lint, strict types and regression tests pass. Public release completion requires the protected CI/CodeQL matrix, tagged artifacts and matching Forge catalog/detail deployment.
