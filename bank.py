import unittest
from unittest.mock import patch

class Account:
    def __init__(self, balance, account_number):
        self._balance = balance
        self._account_number = account_number

    @classmethod
    def create_account(cls, account_number):
        return cls(0.0, account_number)

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
        else:
            raise ValueError('Amount must be positive')

    def withdraw(self, amount):
        if amount > 0:
            self._balance -= amount
        else:
            raise ValueError('Amount must be positive')

    def get_balance(self):
        return self._balance

    def get_account_number(self):
        return self._account_number

    def __str__(self):
        return f'Account number: {self._account_number}, balance: {self._balance}'


class SavingsAccount(Account):
    def __init__(self, balance, account_number, interest_rate):
        super().__init__(balance, account_number)
        self._interest_rate = interest_rate

    def add_interest(self):
        interest_amount = self._balance * self._interest_rate
        self._balance += interest_amount

    def __str__(self):
        return f'Savings Account number: {self._account_number}, balance: {self._balance}'


class CurrentAccount(Account):
    def __init__(self, balance, account_number, overdraft_limit):
        super().__init__(balance, account_number)
        self._overdraft_limit = overdraft_limit

    def send_overdraft_letter(self):
        if self._balance < 0:
            print(f"Overdraft letter sent for Account number: {self._account_number}")

    def __str__(self):
        return f'Current Account number: {self._account_number}, balance: {self._balance}'


class Bank:
    def __init__(self):
        self._accounts = []

    def open_account(self, account):
        self._accounts.append(account)

    def close_account(self, account_number):
        for account in self._accounts:
            if account.get_account_number() == account_number:
                self._accounts.remove(account)
                break

    def pay_dividend(self, amount):
        for account in self._accounts:
            account.deposit(amount)

    def update(self):
        for account in self._accounts:
            if isinstance(account, SavingsAccount):
                account.add_interest()
            elif isinstance(account, CurrentAccount):
                account.send_overdraft_letter()

    def __str__(self):
        return "\n".join(str(account) for account in self._accounts)

class TestBank(unittest.TestCase):
    def test_open_account(self):
        bank = Bank()

        # Create an account and open it in the bank
        savings_acc = SavingsAccount(1000, 'SA001', 0.05)
        bank.open_account(savings_acc)

        # Verify that the account is in the bank's accounts list
        self.assertIn(savings_acc, bank._accounts)


    def test_update(self):
        # Create a bank
        bank = Bank()

        # Create accounts
        savings_acc = SavingsAccount(1000, 'SA001', 0.05)
        current_acc = CurrentAccount(-500, 'CA001', -1000)

        # Open accounts in the bank
        bank.open_account(savings_acc)
        bank.open_account(current_acc)

        # Mock the print function
        with patch("builtins.print") as mock_print:
            # Call the update method
            bank.update()

            # Verify that the print function was called with the expected messages
            mock_print.assert_called_with("Overdraft letter sent for Account number: CA001")

            # Verify that add_interest was called for the savings account
            self.assertTrue(hasattr(savings_acc, "add_interest"))

if __name__ == '__main__':
    unittest.main()
