class Account:
    def __init__(self, account_number, pin, balance):
        self.account_number = account_number
        self.pin = pin
        self.balance = balance

class ATMService:
    def __init__(self):
        # Predefined user accounts (account_number, pin, initial_balance)
        self.accounts = [
            Account("1234", "5678", 1000),
            Account("2345", "6789", 2000),
            Account("3456", "7890", 3000)
        ]
        self.valid_denominations = [100, 200, 500, 2000]
    
    def authenticate(self, account_number, pin):
        """Authenticate user based on account number and PIN"""
        for account in self.accounts:
            if account.account_number == account_number and account.pin == pin:
                return account
        return None

    def validate_amount(self, amount):
        """Validate if amount is a positive integer and uses valid denominations"""
        if not isinstance(amount, int) or amount <= 0:
            return False, "Amount must be a positive integer"
        
        # Check if amount is divisible by smallest denomination (100)
        if amount % 100 != 0:
            return False, "Amount must be in multiples of 100"
            
        return True, "Valid amount"

    def withdraw(self, account, amount):
        """Handle withdrawal logic"""
        # Validate amount
        is_valid, message = self.validate_amount(amount)
        if not is_valid:
            return False, message

        # Check sufficient balance
        if amount > account.balance:
            return False, "Insufficient balance"

        # Calculate denominations
        remaining = amount
        denominations_used = {}
        for denom in sorted(self.valid_denominations, reverse=True):
            if remaining >= denom:
                count = remaining // denom
                denominations_used[denom] = count
                remaining -= count * denom

        # Update balance and return success
        account.balance -= amount
        return True, {
            "message": "Withdrawal successful",
            "denominations": denominations_used,
            "remaining_balance": account.balance
        }

    def deposit(self, account, amount):
        """Handle deposit logic"""
        # Validate amount
        is_valid, message = self.validate_amount(amount)
        if not is_valid:
            return False, message

        account.balance += amount
        return True, {
            "message": "Deposit successful",
            "new_balance": account.balance
        }

    def check_balance(self, account):
        """Return current balance"""
        return account.balance

def main():
    atm = ATMService()
    
    # Login
    print("Welcome to ATM Service")
    account_number = input("Enter account number: ")
    pin = input("Enter PIN: ")
    
    account = atm.authenticate(account_number, pin)
    if not account:
        print("Invalid account number or PIN")
        return

    while True:
        print("\n1. Check Balance")
        print("2. Withdraw Money")
        print("3. Deposit Money")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == "1":
            balance = atm.check_balance(account)
            print(f"Your current balance is: ₹{balance}")

        elif choice == "2":
            try:
                amount = int(input("Enter amount to withdraw: "))
                success, result = atm.withdraw(account, amount)
                if success:
                    print(result["message"])
                    print("Denominations dispensed:")
                    for denom, count in result["denominations"].items():
                        print(f"₹{denom} x {count}")
                    print(f"Remaining balance: ₹{result['remaining_balance']}")
                else:
                    print(f"Error: {result}")
            except ValueError:
                print("Please enter a valid integer amount")

        elif choice == "3":
            try:
                amount = int(input("Enter amount to deposit: "))
                success, result = atm.deposit(account, amount)
                if success:
                    print(result["message"])
                    print(f"New balance: ₹{result['new_balance']}")
                else:
                    print(f"Error: {result}")
            except ValueError:
                print("Please enter a valid integer amount")

        elif choice == "4":
            print("Thank you for using ATM Service")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()