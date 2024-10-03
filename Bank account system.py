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
            
   ''' def add_cash(self, amount):
        if amount > 0:
            self.cash += amount
            with open(f"{name}.txt","r") as f:
                details = f.read()
                self.client_details_list = details.split("\n")
            
            with open(f"{name}.txt","w") as f:
                f.write(details.replace(str(self.client_details_list[3]),str(self.cash)))

            print("Amount added successfully.")

        else:
            print("Enter correct value of amount!")'''

    def tranfer_cash(self, amount , name ,ph):
        with open(f"{name}.txt","r") as f:
            details = f.read()
            self.client_details_list = details.split("\n")
            if str(ph) in self.client_details_list:
                self.TranferCash = True

        
        if self.TranferCash == True:
            total_cash = int(self.client_details_list[3]) + amount
            left_cash = self.cash - amount
            with open(f"{name}.txt","w") as f:
                f.write(details.replace(str(self.client_details_list[3]),str(total_cash)))

            with open(f"{self.name}.txt","r") as f:
                details_2 = f.read()
                self.client_details_list = details.split("\n")
            
            with open(f"{self.name}.txt","w") as f:
                f.write(details_2.replace(str(self.client_details_list[3]),str(left_cash)))

            print("Amount Transfered Successfully to",name,"-",ph)
            print("Balacne left =",left_cash)
    
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
        
    def ph_change(self , ph):
        if len(str(ph)) > 10 or len(str(ph)) < 10:
            print("Invalid Phone number ! please enter 10 digit number")
        else:
            with open(f"{self.name}.txt","r") as f:
                details = f.read()
                self.client_details_list = details.split("\n")

            with open(f"{self.name}.txt","w") as f:
                f.write(details.replace(str(self.client_details_list[1]),str(ph)))
            print("New Phone number set up successfully")



if __name__ == "__main__":
    Bank_object = Bank()
    print("\t\t\tWelcome to our Bank!!")
    print("1.Login.")
    print("2.Create a new Account.")
    user = int(input("Make decision: "))

    if user == 1:
        print("Logging in")
        name = input("Enter Name: ")
        ph = int(input("Enter Phone Number: "))
        password = input("Enter password: ")
        Bank_object.login(name, ph, password)
        while True:
            if Bank_object.loggedin:
                print("1.Add amount")
                print("2.Check Balance")
                print("3.Tranfer amount")
                print("4.Edit profile")
                print("5.Logout")
                login_user = int(input())
                if login_user == 1:
                    print("Balance =",Bank_object.cash)
                    amount = int(input("Enter amount: "))
                    Bank_object.add_cash(amount)
                    print("\n1.Back menu")
                    print("2.Logout")
                    choose = int(input())
                    if choose == 1:
                        continue
                    elif choose == 2:
                        break
                
                elif login_user == 2:
                    print("Balacne =",Bank_object.cash)
                    print("\n1.Back menu")
                    print("2.Logout")
                    choose = int(input())
                    if choose == 1:
                        continue
                    elif choose == 2:
                        break

                elif login_user == 3:
                    print("Balance =",Bank_object.cash)
                    amount = int(input("Enter amount: "))
                    if amount >= 0 and amount <= Bank_object.cash:
                        name = input("Enter person name: ")
                        ph = input("Enter person phone number: ")
                        Bank_object.Tranfer_cash(amount,name,ph)
                        print("\n1.Back menu")
                        print("2.Logout")
                        choose = int(input())
                        if choose == 1:
                            continue
                        elif choose == 2:
                            break
                    elif amount < 0 :
                        print("Please Enter correct value of amount")

                    elif amount > Bank_object.cash:
                        print("Not enough balance")

                elif login_user == 4:
                    print("1.Password change")
                    print("2.Phone Number change")
                    edit_profile = int(input())
                    if edit_profile == 1:
                        new_passwrod = input("Enter new Password: ")
                        Bank_object.password_change(new_passwrod)
                        print("\n1.Back menu")
                        print("2.Logout")
                        choose = int(input())
                        if choose == 1:
                            continue
                        elif choose == 2:
                            break
                    elif edit_profile == 2:
                        new_ph = int(input("Enter new Phone Number: "))
                        Bank_object.ph_change(new_ph)
                        print("\n1.Back menu")
                        print("2.Logout")
                        choose = int(input())
                        if choose == 1:
                            continue
                        elif choose == 2:
                            break

                elif login_user == 5:
                    break
                        
                
    if user == 2:
        print("Creating a new  Account")
        name = input("Enter Name: ")
        ph = int(input("Enter Phone Number: "))
        password = input("Enter password: ")
        Bank_object.register(name, ph, password)


#changes to make in the code: 
# Fix method naming
# Better error handling
# Input validations for phone numbers and amount, etc.
# Password hashing using hashlib
# Consolidate read/write file operations
# add transaction history