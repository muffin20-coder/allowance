"""Data models used by the allowance planner."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Iterable, List


ALLOWED_CATEGORIES = ("save", "spend", "share", "need")


@dataclass
class AllowancePlan:
    """Represents the way an allowance is divided between categories."""

    income: float
    allocation: Dict[str, float]

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if self.income < 0:
            raise ValueError("Income must be non-negative.")
        for category, amount in self.allocation.items():
            if category not in ALLOWED_CATEGORIES:
                raise ValueError(f"Unknown category: {category}")
            if amount < 0:
                raise ValueError("Allocated amounts must be non-negative.")
        total = sum(self.allocation.values())
        if total > self.income + 1e-9:
            raise ValueError(
                "Allocated amounts cannot exceed the total allowance income."
            )

    @property
    def unallocated(self) -> float:
        """Return the amount of income that has not yet been allocated."""

        return self.income - sum(self.allocation.values())

    def category_amount(self, category: str) -> float:
        """Return the planned amount for *category* or 0 if missing."""

        return self.allocation.get(category, 0.0)


@dataclass
class Transaction:
    """Represents a planned or actual allowance transaction."""

    category: str
    amount: float
    description: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        if self.category not in ALLOWED_CATEGORIES:
            raise ValueError(f"Unknown category: {self.category}")
        if self.amount < 0:
            raise ValueError("Transaction amount must be non-negative.")


@dataclass
class AllowanceState:
    """Serializable structure describing an allowance plan and its usage."""

    plan: AllowancePlan
    transactions: List[Transaction]

    def by_category(self, category: str) -> Iterable[Transaction]:
        return (txn for txn in self.transactions if txn.category == category)

    def spent_for(self, category: str) -> float:
        return sum(txn.amount for txn in self.by_category(category))

    def remaining_for(self, category: str) -> float:
        return self.plan.category_amount(category) - self.spent_for(category)
