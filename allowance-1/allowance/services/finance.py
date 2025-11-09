from decimal import Decimal

class FinanceService:
    def __init__(self):
        self.balance = Decimal('0.00')

    def add_transaction(self, amount: Decimal):
        self.balance += amount

    def subtract_transaction(self, amount: Decimal):
        self.balance -= amount

    def get_balance(self) -> Decimal:
        return self.balance

    def calculate_allowance(self, allowance_rate: Decimal, period: int) -> Decimal:
        return allowance_rate * period

    def apply_allowance(self, allowance_rate: Decimal, period: int):
        allowance = self.calculate_allowance(allowance_rate, period)
        self.add_transaction(allowance)