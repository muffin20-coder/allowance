from __future__ import annotations

from pathlib import Path

from allowance.planner import AllowanceLedger


def test_plan_and_transactions(tmp_path: Path) -> None:
    storage = tmp_path / "data.json"
    ledger = AllowanceLedger.load(storage)

    plan = ledger.set_plan(20.0, {"save": 5.0, "spend": 10.0, "share": 3.0})
    assert plan.income == 20.0
    assert plan.category_amount("save") == 5.0
    assert plan.unallocated == 2.0

    ledger.add_transaction("spend", 4.0, "Snacks")
    ledger.add_transaction("save", 2.0)

    assert ledger.spent_amount("spend") == 4.0
    assert round(ledger.remaining_amount("save"), 2) == 3.0

    ledger2 = AllowanceLedger.load(storage)
    assert ledger2.spent_amount("save") == 2.0
    assert ledger2.state.plan.category_amount("share") == 3.0
