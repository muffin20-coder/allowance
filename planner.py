"""High level interface for managing an allowance plan."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Optional

from .models import ALLOWED_CATEGORIES, AllowancePlan, AllowanceState, Transaction
from .storage import DEFAULT_STORAGE_FILE, load_state, save_state


@dataclass
class AllowanceLedger:
    """Wraps :class:`AllowanceState` with helper operations."""

    state: AllowanceState
    storage_path: Path = DEFAULT_STORAGE_FILE

    @classmethod
    def load(cls, path: Optional[Path] = None) -> "AllowanceLedger":
        storage_path = path or DEFAULT_STORAGE_FILE
        state = load_state(storage_path)
        return cls(state=state, storage_path=storage_path)

    def save(self) -> None:
        save_state(self.state, self.storage_path)

    # Plan operations -------------------------------------------------
    def set_plan(self, income: float, allocations: Dict[str, float]) -> AllowancePlan:
        plan = AllowancePlan(income=income, allocation=allocations)
        self.state.plan = plan
        self.save()
        return plan

    # Transaction operations -----------------------------------------
    def add_transaction(
        self, category: str, amount: float, description: str = ""
    ) -> Transaction:
        transaction = Transaction(category=category, amount=amount, description=description)
        self.state.transactions.append(transaction)
        self.save()
        return transaction

    def clear_transactions(self) -> None:
        self.state.transactions.clear()
        self.save()

    # Reporting -------------------------------------------------------
    def planned_amount(self, category: str) -> float:
        return self.state.plan.category_amount(category)

    def spent_amount(self, category: str) -> float:
        return self.state.spent_for(category)

    def remaining_amount(self, category: str) -> float:
        return self.state.remaining_for(category)

    def iter_categories(self) -> Iterable[str]:
        """Return the categories that appear in the plan or transactions.

        The order favours the predefined :data:`ALLOWED_CATEGORIES` so the
        command line reports stay familiar, but any additional categories will be
        appended alphabetically.
        """

        used_categories = set(self.state.plan.allocation.keys())
        used_categories.update(txn.category for txn in self.state.transactions)
        if not used_categories:
            return tuple(ALLOWED_CATEGORIES)

        ordered = [c for c in ALLOWED_CATEGORIES if c in used_categories]
        custom = sorted(used_categories.difference(ALLOWED_CATEGORIES))
        return tuple(ordered + custom)


def load_ledger(path: Optional[Path] = None) -> AllowanceLedger:
    """Convenience helper mirroring :meth:`AllowanceLedger.load`."""

    return AllowanceLedger.load(path)
