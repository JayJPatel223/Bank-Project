import hashlib
import os

class Bank:
    def __init__(self):
        self.client_details_list = []
        self.loggedin = False
        self.cash = 100
        self.tranfercash = False
        self.name = ""

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_phone(self, ph):
        return str(ph).isdigit() and len(str(ph)) == 10


    def register(self, name, ph, password):
        cash = self.cash
        conditions = True

        if not self.validate_phone(ph):
            print("Invalid Phone number! Please enter a valid 10-digit number.")
            conditions = False

        if len(password) < 5 or len(password) > 18:
            print("Password must be between 5 and 18 characters.")
            conditions = False

        if conditions:
            print("Account created successfully!")
            hashed_password = self.hash_password(password)
            self.client_details_list = [name, ph, hashed_password, str(cash)]
            with open(f"{name}.txt", "w") as f:
                for details in self.client_details_list:
                    f.write(details + "\n")
            # Create an empty transaction history
            with open(f"{name}_transactions.txt", "w") as f:
                f.write("Transaction History\n")

    def login(self, name, ph, password):
        try:
            with open(f"{name}.txt", "r") as f:
                details = f.read().split("\n")
                self.client_details_list = details
                stored_password_hash = details[2]
                password_hash = self.hash_password(password)

                if str(ph) == details[1] and password_hash == stored_password_hash:
                    self.loggedin = True
                    self.cash = int(details[3])
                    self.name = name
                    print(f"{name} logged in successfully!")
                else:
                    print("Incorrect phone number or password.")
        except FileNotFoundError:
            print("Account not found!")
    
    def add_cash(self, amount):
        if amount > 0:
            self.cash += amount
            self.update_file_balance()
            self.log_transaction(f"Added {amount}. New Balnace: {self.cash}")
            print("Amount added succesfully.")
        else:
            print("Enter a valid amount!")
            
    def tranfer_cash(self, amount, recipent_name, recipent_ph):
        if amount > self.cash or amount <= 0:
            print("Invalid transfer amount.")
            return
        try: 
            with open(f"{recipent_name}.txt", "r") as f:
                details = f.read().spilt("\n")
                if str(recipent_ph) == details[1]:
                    recipent_cash = int(details[3])
                    recipent_cash += amount

                    with open(f"{recipent_name}.txt", "w") as f:
                        details[3] = str(recipent_cash)
                        f.write("\n".join(details))

                        self.cash -= amount
                        self.update_file_balance()

                        self.log_transaction(f"Transferred {amount} to {recipient_name}. New balance: {self.cash}")
                        print(f"Transferred {amount} to {recipient_name}. New balance: {self.cash}")
                else:
                        print("Recipent details are incorrect.")
        except FileNotFoundError:
            print("Recipent account not found.")

    def password_change(self, password):
        if len(password) < 5 or len(password) > 18:
            print("Enter password greater than 5 and less than 18 character")
        else:
            with open(f"{self.name}.txt","r") as f:
                details = f.read()
                self.client_details_list = details.split("\n")

            with open(f"{self.name}.txt","w") as f:
                f.write(details.replace(str(self.client_details_list[2]),str(password)))
            print("New Password set up successfully")
    
    def update_file_balance(self):
        with open(f"{self.name}.txt", "r") as f:
            details = f.read().split("\n")
        details[3] = str(self.cash)
        with open(f"{self.name}.txt", "w") as f:
            f.write("\n".join(details))       
        
    def log_transaction(self, message):
        with open(f"{self.name}_transaction.txt", "a") as f:
            f.write(f"{message}\n")

    def view_transaction_history(self):
        try:
            with open(f"{self.name}_transaction.txt", "r") as f:
                history = f.read()
                print(history)
        except FileNotFoundError:
            print("Transaction history not found.")

    def password_change(self, new_password):
        if len(new_password) < 5 or len(new_password) > 18:
            print("Password must be between 5 and 18 characters.")
        else:
            with open(f"{self.name}.txt","r") as f:
                details = f.read().split("\n")
            hashed_password = self.hash_password(new_password)
            details[2] = hashed_password
            with open(f"{self.name}.txt","w") as f:
                f.write("\n".join(details))
            print("Password changed successfully")
            self.log_transaction("password changed.")


    def ph_change(self ,new_ph):
        if not self.validate_phone(new_ph):
            print("Invalid Phone number! Please enter a valid 10-digit number.")
        else:
            with open(f"{self.name}.txt", "r") as f:
                details = f.read().split("\n")
            details[1] = str(new_ph)
            with open(f"{self.name}.txt", "w") as f:
                f.write("\n".join(details))
            print("Phone number changed successfully.")
            self.log_transaction("Phone number changed.")



if __name__ == "__main__":
    bank = Bank()
    print("\t\t\tWelcome to our Bank!!")
    print("1. Login.")
    print("2. Create a new Account.")
    
    user_choice = int(input("Make your choice: "))

    if user_choice == 1:
        name = input("Enter Name: ")
        ph = input("Enter Phone Number: ")
        password = input("Enter Password: ")
        bank.login(name, ph, password)
        if bank.loggedin:
            while True:
                print("\n1. Add Amount")
                print("2. Check Balance")
                print("3. Transfer Amount")
                print("4. View Transaction History")
                print("5. Edit Profile")
                print("6. Logout")
                
                choice = int(input("Choose an option: "))
                if choice == 1:
                    print(f"Current Balance: {bank.cash}")
                    amount = int(input("Enter amount to add: "))
                    bank.add_cash(amount)

                elif choice == 2:
                    print(f"Balance: {bank.cash}")

                elif choice == 3:
                    recipient_name = input("Enter recipient's name: ")
                    recipient_ph = input("Enter recipient's phone number: ")
                    amount = int(input("Enter amount to transfer: "))
                    bank.transfer_cash(amount, recipient_name, recipient_ph)

                elif choice == 4:
                    bank.view_transaction_history()

                elif choice == 5:
                    print("1. Change Password")
                    print("2. Change Phone Number")
                    edit_choice = int(input())
                    if edit_choice == 1:
                        new_password = input("Enter new password: ")
                        bank.password_change(new_password)
                    elif edit_choice == 2:
                        new_ph = input("Enter new phone number: ")
                        bank.ph_change(new_ph)

                elif choice == 6:
                    print("Logged out.")
                    break

    elif user_choice == 2:
        name = input("Enter Name: ")
        ph = input("Enter Phone Number: ")
        password = input("Enter Password: ")
        bank.register(name, ph, password)

#changes to make in the code: 
# Fix method naming (done)
# Better error handling (done)
# Input validations for phone numbers and amount, etc. (done)
# Password hashing using hashlib (done)
# Consolidate read/write file operations (done)
# add transaction history (done)