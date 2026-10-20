# Development contract

Create spoiler-controlled return-to-reading cards for pauses within a book or series.

Preserve deterministic, source-safe behavior and the interpretation boundary documented in the README. Every feature release must update tests, version metadata, changelog, README claims, repository metadata, release assets, and the Forge catalog together.

## 1.2.0 improvement session

Validate nested checkpoint records and add printable pocket/phone cards with checkpoint previews and hidden-item counts.

Work and display fields must be text; milestone/checkpoint fields must be nonnegative integers, excluding booleans. Event, character and thread records are validated before filtering. HTML supports phone and pocket-print layouts and earlier checkpoint previews, with counts of newly included and still-hidden items. Future text and unsupported extra fields are excluded from the export; only hidden-item counts remain. To advance beyond the exported ceiling, update the private input's through checkpoint and regenerate. The page does not modify the original input.

Local formatting, lint, strict types and regression tests pass. Public release completion requires the protected CI/CodeQL matrix, tagged artifacts and matching Forge catalog/detail deployment.

## Thread resolution milestones

Version 1.3.0 accepts an optional `resolution_milestone` on a thread with
`status: "resolved"`. It must be an integer at or after the thread's `milestone`.
For example, `{"text": "Who sent the letter?", "milestone": 2, "status": "resolved",
"resolution_milestone": 8}` remains open through checkpoint 7 and resolves at 8.
Keep thread text safe from its first milestone; this field schedules status, not
a separate resolution narrative. Dates and resolutions are never inferred.

Resolution metadata beyond `through` is omitted from JSON, Markdown and HTML.
Earlier HTML previews calculate status at the selected checkpoint; the exported
ceiling still limits available facts. Resolution changes after `previous_checkpoint`
are included in thread deltas once visible. Omitting the field preserves the
existing behavior: status applies at the thread's original milestone.

## Version 1.3.1

Select the five most recent visible events by supplied milestone, retaining authored order for ties. Create outputs exclusively so existing files and symbolic-link destinations remain untouched.
