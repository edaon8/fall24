# Code courtesy of Zander
#!/usr/bin/env python3

from dataclasses import dataclass
import random
import string

@dataclass
class Account:
    number: int
    name: str
    password: str
    balance: int

    @staticmethod
    def new(name: str, balance=0) -> "Account":
        number = random.randint(100000000, 999999999)
        password = "".join([random.choice(string.ascii_lowercase + string.digits) for _ in range(10)])

        return Account(number, name, password, balance)
    
    def transfer_to(self, dest: "Account", amount: int) -> bool:
        if self.balance < amount:
            print("Not enough money in the account for this transfer!")
            return False
        
        self.balance -= amount
        dest.balance += amount

        return True
    
    def __str__(self) -> str:
        return f"Account #{self.number} ({self.name}), balance ${self.balance}"
    
ACTIVE_ACCOUNT: Account | None = None
ACCOUNTS: list[Account] = []
DEV_MODE = False

def init_accounts():
    if len(ACCOUNTS) > 0:
        return
    
    ACCOUNTS.append(Account.new("Brandon", balance=random.randint(100,500)))
    ACCOUNTS.append(Account.new("Dave", balance=random.randint(100,500)))
    ACCOUNTS.append(Account.new("Kevin", balance=random.randint(100,500)))

def menu():
    print("--- Menu ---")
    print(" 1) Show Accounts")
    print(" 2) Add New Account")
    print(" 3) Login to Account")
    print(" 4) Transfer Amount")
    print(" 5) Exit")

def show_accounts():
    [print(acct) for acct in ACCOUNTS]
    print("")

def add_account():
    name = input("Name: ")

    acct = Account.new(name)
    ACCOUNTS.append(acct)

    print(f"Account added (number: {acct.number}, password: {acct.password})")

def lookup_acct(number: str | int) -> Account | None:
    try:
        return list(filter(lambda x: x.number == int(number), ACCOUNTS))[0]
    except (IndexError, ValueError):
        print("Invalid account number!")
        return

def login_to_account():
    number = input("Account Number: ")
    acct = lookup_acct(number)
    if acct is None:
        return
    
    passwd = input("Password: ")

    if acct.password in passwd:
        global ACTIVE_ACCOUNT
        ACTIVE_ACCOUNT = acct
        if passwd.endswith("DEVMODE"):
            print("**** DEV MODE ****")
            global DEV_MODE
            DEV_MODE = True

        print("Logged into account")

        return

def do_transfer():
    if DEV_MODE:
        number = input("Source Account Number: ")
        src_acct = lookup_acct(number)
        if src_acct is None:
            return
    else:
        if ACTIVE_ACCOUNT is None:
            print("No account logged in!")
            return
        
        src_acct = ACTIVE_ACCOUNT

    dest_number = input("Destination Account Number: ")
    dest_acct = lookup_acct(dest_number)
    if dest_acct is None:
        return

    try:
        amount = int(input("Enter amount to transfer: "))
    except ValueError:
        print("Invalid amount!")
        return
    
    src_acct.transfer_to(dest_acct, amount)

def repl():
    while True:
        menu()
        try:
            choice = int(input("Choice: "))
        except ValueError:
            continue

        print("")
        if choice == 1:
            show_accounts()
        elif choice == 2:
            add_account()
        elif choice == 3:
            login_to_account()
        elif choice == 4:
            do_transfer()
        elif choice == 5:
            return

def main():
    init_accounts()
    repl()

if __name__ == "__main__":
    main()