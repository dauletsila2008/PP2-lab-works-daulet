class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient Funds"
        self.balance -= amount
        return self.balance


initial_balance, withdrawal_amount = map(int, input().split())

account = Account("User", initial_balance)

result = account.withdraw(withdrawal_amount)
print(result)