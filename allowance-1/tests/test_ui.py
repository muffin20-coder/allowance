import unittest
from allowance.ui.main_window import MainWindow
from allowance.ui.components.balance_view import BalanceView
from allowance.ui.components.transaction_form import TransactionForm

class TestUIComponents(unittest.TestCase):

    def setUp(self):
        self.main_window = MainWindow()
        self.balance_view = BalanceView()
        self.transaction_form = TransactionForm()

    def test_main_window_initialization(self):
        self.assertIsNotNone(self.main_window)
        self.assertTrue(self.main_window.is_visible())

    def test_balance_view_display(self):
        self.balance_view.set_balance(100)
        self.assertEqual(self.balance_view.get_balance(), 100)

    def test_transaction_form_submission(self):
        self.transaction_form.set_amount(50)
        self.transaction_form.set_description("Test transaction")
        result = self.transaction_form.submit()
        self.assertTrue(result)
        self.assertEqual(self.transaction_form.get_amount(), 50)
        self.assertEqual(self.transaction_form.get_description(), "Test transaction")

if __name__ == '__main__':
    unittest.main()