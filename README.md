# allowance
# Allowance planner

This repository provides a small Python command line program that helps a family
plan how an allowance will be used. The tool lets you document a weekly income,
assign how much should go to each category (Save, Spend, Share, Need), track the
money that has been used, and show a quick progress summary.

## Installation

The project uses a standard Python package layout and exposes an `allowance`
console script. You can install it in editable mode while you experiment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --editable .
```

> **Tip**: If you do not want to install the package, you can also invoke the
> tool directly with `python -m allowance` from the repository root.

## Usage

Create or update an allowance plan by specifying the total income along with any
category amounts that you want to reserve.

```bash
allowance plan 20 --save 5 --spend 10 --share 3
```

Record transactions whenever money is used from one of the categories:

```bash
allowance record spend 4 "Snacks with friends"
```

See where the allowance currently stands:

```bash
allowance summary
```

Reset recorded transactions (and optionally the plan) when you want to start
fresh:

```bash
allowance reset
allowance reset --everything
```

The program stores its data in `~/.allowance.json` by default. Use the
`--storage` flag with any command to change the location of the data file.

## Contributor Guide

New contributors should review `AGENTS.md` for repository structure, coding
style, testing expectations, and pull request conventions before opening
changes.

## Web UI Smoke Test

The static UI under `allowance/web/` now has an automated regression in
`tests/test_web_ui.py` that relies on Playwright.

```bash
pip install pytest playwright
playwright install
pytest tests/test_web_ui.py -k web_ui
```

The test starts a lightweight HTTP server, verifies that memo edits persist
after a reload, and checks that footer totals update when new transactions are
recorded.
