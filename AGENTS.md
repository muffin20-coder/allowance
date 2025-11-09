# Repository Guidelines

## Project Structure & Module Organization
Source lives under `allowance/`, with the CLI entry point in `allowance/cli.py`, core models and persistence in `models.py`, `planner.py`, and `storage.py`, plus a lightweight web stub in `allowance/web/`. Tests sit in `tests/` (currently `tests/test_planner.py`). Packaging metadata and console entry points are managed through `pyproject.toml`, while the README summarizes the CLI.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate`: create/enter the local virtualenv expected by other contributors.
- `pip install --editable .`: install the CLI in editable mode so changes are picked up immediately.
- `python -m allowance summary` (or `allowance summary` once installed): run the CLI against the default `~/.allowance.json` store.
- `python -m pytest -q`: execute the automated tests; keep runs focused and quiet for CI readability.

## Coding Style & Naming Conventions
Code targets Python 3.10+, with 4-space indentation, `snake_case` functions, and `PascalCase` classes (e.g., `AllowanceLedger`). Favor dataclasses for state containers, keep module imports explicit (`from allowance import ...`), and stick with type hints already established. JSON storage keys should mirror attribute names to simplify serialization.

## Testing Guidelines
Pytest is the framework of record; name files `test_*.py` and functions `test_*`. Use fixtures like `tmp_path` for filesystem work so tests remain hermetic. Extend functional coverage around planner behaviors (plan validation, transaction math, persistence) before landing features. Always run `python -m pytest` locally; if adding new commands, include representative CLI tests or document manual verification.

## Commit & Pull Request Guidelines
Existing history uses short, imperative commit subjects (“Add Allowance CLI + Web UI”). Match that style, grouping logical changes together and mentioning the main component touched. Pull requests should describe the motivation, summarize visible changes (CLI flags, storage schema, etc.), note any testing done, and include screenshots or sample CLI output when user-facing behavior changes. Link issues or TODO references where applicable and call out breaking changes explicitly.

## Storage & Configuration Tips
By default the ledger persists to `~/.allowance.json`. When testing, redirect with `--storage path/to/tmp.json` to avoid mutating personal data, and reset via `allowance reset --everything` before capturing “clean” examples. Keep secrets out of the repo—only JSON fixture data belongs under version control.
