"""Persistence helpers for the allowance planner."""
from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
from typing import Any, Dict

from .models import AllowancePlan, AllowanceState, Transaction

DEFAULT_STORAGE_FILE = Path.home() / ".allowance.json"


def _serialize_transaction(txn: Transaction) -> Dict[str, Any]:
    return {
        "category": txn.category,
        "amount": txn.amount,
        "description": txn.description,
        "timestamp": txn.timestamp.isoformat(),
    }


def _deserialize_transaction(data: Dict[str, Any]) -> Transaction:
    timestamp = data.get("timestamp")
    return Transaction(
        category=data["category"],
        amount=float(data["amount"]),
        description=data.get("description", ""),
        timestamp=datetime.fromisoformat(timestamp) if timestamp else datetime.utcnow(),
    )


def _serialize_plan(plan: AllowancePlan) -> Dict[str, Any]:
    return {
        "income": plan.income,
        "allocation": plan.allocation,
    }


def _deserialize_plan(data: Dict[str, Any]) -> AllowancePlan:
    return AllowancePlan(
        income=float(data.get("income", 0.0)),
        allocation={k: float(v) for k, v in data.get("allocation", {}).items()},
    )


def load_state(path: Path = DEFAULT_STORAGE_FILE) -> AllowanceState:
    """Load a previously saved allowance state or return an empty one."""

    if path.exists():
        payload = json.loads(path.read_text())
        plan_data = payload.get("plan", {})
        plan = _deserialize_plan(plan_data)
        transactions = [_deserialize_transaction(item) for item in payload.get("transactions", [])]
    else:
        plan = AllowancePlan(income=0.0, allocation={})
        transactions = []
    return AllowanceState(plan=plan, transactions=transactions)


def save_state(state: AllowanceState, path: Path = DEFAULT_STORAGE_FILE) -> None:
    """Persist *state* to *path* in JSON format."""

    payload = {
        "plan": _serialize_plan(state.plan),
        "transactions": [_serialize_transaction(txn) for txn in state.transactions],
    }
    path.write_text(json.dumps(payload, indent=2))

