# Changelog

## 1.3.2 - 2026-10-20

- Include development and testing instructions in source distributions. The preceding 1.3.1 tag was held before public release when distribution acceptance found these missing files.

## 1.3.1 - 2026-10-20 (unpublished tag)

- Select the five most recent visible events by supplied milestone, retaining authored order for ties. Create outputs exclusively so existing files and symbolic-link destinations remain untouched.

- Markdown treats supplied text as literal, single-line content so notes cannot introduce HTML or forged checklist headings. JSON retains the original text.

## 1.3.0 - 2026-10-16

- Added explicit thread resolution milestones, checkpoint-safe status and resolution deltas.
- Kept future resolution metadata outside exported cards and preserved legacy thread behavior.

## 1.2.0 - 2026-09-07

- Validate nested checkpoint records and add printable pocket/phone cards with checkpoint previews and hidden-item counts.
- Added regression coverage for the audited behavior and invalid inputs.

## 1.1.0 - 2026-07-27

- Added open and resolved thread separation plus importance levels.
- Added changes-since-checkpoint summaries and stricter milestone validation.
- Replaced generic data blocks with a purpose-built reading resume card.

## 1.0.0 - 2026-07-26

- Released the first complete Reading Resume Card Generator command-line workflow.
- Added deterministic reporting, representative examples, cross-platform tests, and explicit limitations.
