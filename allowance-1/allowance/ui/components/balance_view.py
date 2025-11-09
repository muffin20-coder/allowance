from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class BalanceView(QWidget):
    def __init__(self, balance=0.0):
        super().__init__()
        self.balance = balance
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.balance_label = QLabel(f"Current Balance: ${self.balance:.2f}")
        layout.addWidget(self.balance_label)

        self.setLayout(layout)
        self.setWindowTitle("Balance View")
        self.show()

    def update_balance(self, new_balance):
        self.balance = new_balance
        self.balance_label.setText(f"Current Balance: ${self.balance:.2f}")