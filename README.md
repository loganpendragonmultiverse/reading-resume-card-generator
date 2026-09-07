# Reading Resume Card Generator

[![CI](https://github.com/loganpendragonmultiverse/reading-resume-card-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/reading-resume-card-generator/actions/workflows/ci.yml)

Create spoiler-controlled return-to-reading cards for pauses within a book or series. The command uses explicit UTF-8 JSON input and produces reviewable JSON or Markdown output.

## Three-minute start

```bash
python -m pip install .
reading-resume-cards examples/sample.json
reading-resume-cards examples/sample.json --format json --output report.json
```

The example documents the v1 input shape. Existing report files are never overwritten. Source inputs are read-only except where the documented purpose explicitly creates a new output artifact.

Version 1.1 adds `previous_checkpoint`, `importance` (`low`, `medium`, `high`, or `critical`), and thread `status` (`open` or `resolved`). Markdown output is now a purpose-built resume card with recent events, character reminders, separate thread lists, changes since the previous checkpoint, and the next reading step.

## Privacy and platforms

The tool runs locally and does not upload input or include telemetry. Python 3.10 or newer is supported on Windows, macOS, and Linux.

## Interpretation boundary

Spoiler safety depends on accurate milestone numbers in supplied data. The tool does not infer canon or read a book.

## Development

```bash
python -m pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy src
pytest
python -m build
```

Release metadata must stay aligned across the package, changelog, GitHub release, and Logan Pendragon Forge catalog.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).

## Version 1.2.0: reviewed improvements

Validate nested checkpoint records and add printable pocket/phone cards with checkpoint previews and hidden-item counts.

```bash
reading-resume-cards examples/sample.json --format html --output card.html
```

Work and display fields must be text; milestone/checkpoint fields must be nonnegative integers, excluding booleans. Event, character and thread records are validated before filtering. HTML supports phone and pocket-print layouts and earlier checkpoint previews, with counts of newly included and still-hidden items. Future text and unsupported extra fields are excluded from the export; only hidden-item counts remain. To advance beyond the exported ceiling, update the private input's through checkpoint and regenerate. The page does not modify the original input.
