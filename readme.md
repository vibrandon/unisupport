original singleton code
```
class InsufficientBalance(Exception):
    pass


class AccountNumberGenerator:
    _instance = None
    _account_number = 10012

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AccountNumberGenerator, cls).__new__(cls)
        return cls._instance

    def get_new_account_number(self):
        AccountNumberGenerator._account_number += 1
        return AccountNumberGenerator._account_number


class Account:
    def __init__(self, account_name):
        account_gen = AccountNumberGenerator()
        self.account_name = account_name
        self.account_number = account_gen.get_new_account_number()
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance < amount:
            raise InsufficientBalance("Insufficient balance in account.")
        self.balance -= amount
        return amount

    def check_balance(self):
        return self.balance
```