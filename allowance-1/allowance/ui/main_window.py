from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from allowance.ui.components.balance_view import BalanceView
from allowance.ui.components.transaction_form import TransactionForm

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Allowance CLI")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.balance_view = BalanceView()
        self.transaction_form = TransactionForm()

        self.layout.addWidget(self.balance_view)
        self.layout.addWidget(self.transaction_form)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())