"""Command line interface for the allowance planner."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict

from .models import ALLOWED_CATEGORIES
from .planner import AllowanceLedger


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage a simple allowance plan.")
    parser.add_argument(
        "--storage",
        type=Path,
        default=None,
        help="Path to the JSON file where allowance data will be stored.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser(
        "plan", help="Create or update the allowance plan allocations."
    )
    plan_parser.add_argument("income", type=float, help="Total allowance income.")
    for category in ALLOWED_CATEGORIES:
        plan_parser.add_argument(
            f"--{category}",
            type=float,
            default=None,
            help=f"Amount allocated to the '{category}' category.",
        )

    record_parser = subparsers.add_parser(
        "record", help="Record a new transaction for a category."
    )
    record_parser.add_argument("category", choices=ALLOWED_CATEGORIES)
    record_parser.add_argument("amount", type=float)
    record_parser.add_argument("description", nargs="*", help="Optional description.")

    subparsers.add_parser("summary", help="Show the current plan and progress.")

    reset_parser = subparsers.add_parser(
        "reset", help="Remove recorded transactions (optionally the plan too)."
    )
    reset_parser.add_argument(
        "--everything",
        action="store_true",
        help="Remove the saved plan in addition to transactions.",
    )

    return parser


def _collect_allocations(args: argparse.Namespace) -> Dict[str, float]:
    allocations: Dict[str, float] = {}
    for category in ALLOWED_CATEGORIES:
        value = getattr(args, category)
        if value is not None:
            allocations[category] = value
    return allocations


def _ledger_from_args(args: argparse.Namespace) -> AllowanceLedger:
    return AllowanceLedger.load(args.storage)


def cmd_plan(args: argparse.Namespace) -> str:
    allocations = _collect_allocations(args)
    ledger = _ledger_from_args(args)
    plan = ledger.set_plan(args.income, allocations)
    lines = [
        "Allowance plan saved:",
        f"  Income: {plan.income:.2f}",
    ]
    for category in ledger.iter_categories():
        lines.append(
            f"  {category.title():<8}: {plan.category_amount(category):.2f}"
        )
    if plan.unallocated > 0:
        lines.append(f"  Unallocated: {plan.unallocated:.2f}")
    return "\n".join(lines)


def cmd_record(args: argparse.Namespace) -> str:
    description = " ".join(args.description) if args.description else ""
    ledger = _ledger_from_args(args)
    txn = ledger.add_transaction(args.category, args.amount, description)
    return (
        f"Recorded {txn.amount:.2f} to {txn.category}."
        + (f" Note: {txn.description}" if txn.description else "")
    )


def cmd_summary(args: argparse.Namespace) -> str:
    ledger = _ledger_from_args(args)
    plan = ledger.state.plan
    lines = ["Current allowance summary:"]
    lines.append(f"  Income: {plan.income:.2f}")
    for category in ledger.iter_categories():
        planned = ledger.planned_amount(category)
        spent = ledger.spent_amount(category)
        remaining = planned - spent
        lines.append(
            f"  {category.title():<8} Planned: {planned:6.2f} | Spent: {spent:6.2f} | Remaining: {remaining:6.2f}"
        )
    if plan.unallocated > 0:
        lines.append(f"  Unallocated funds: {plan.unallocated:.2f}")
    if not ledger.state.transactions:
        lines.append("  No transactions recorded yet.")
    return "\n".join(lines)


def cmd_reset(args: argparse.Namespace) -> str:
    ledger = _ledger_from_args(args)
    ledger.clear_transactions()
    message = "All recorded transactions have been removed."
    if args.everything:
        ledger.set_plan(0.0, {})
        message = "All transactions and the allowance plan have been removed."
    return message


def main(argv: list[str] | None = None) -> str:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "plan":
        output = cmd_plan(args)
    elif args.command == "record":
        output = cmd_record(args)
    elif args.command == "summary":
        output = cmd_summary(args)
    elif args.command == "reset":
        output = cmd_reset(args)
    else:
        parser.error("Unknown command")
        raise SystemExit(2)

    print(output)
    return output


if __name__ == "__main__":
    main()
