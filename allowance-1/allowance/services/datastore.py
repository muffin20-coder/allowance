from typing import List, Dict
import json
import os

class DataStore:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self) -> Dict:
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return {}

    def save_data(self) -> None:
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    def get_balance(self) -> float:
        return self.data.get('balance', 0.0)

    def update_balance(self, amount: float) -> None:
        self.data['balance'] = self.get_balance() + amount
        self.save_data()

    def add_transaction(self, transaction: Dict) -> None:
        if 'transactions' not in self.data:
            self.data['transactions'] = []
        self.data['transactions'].append(transaction)
        self.save_data()

    def get_transactions(self) -> List[Dict]:
        return self.data.get('transactions', [])