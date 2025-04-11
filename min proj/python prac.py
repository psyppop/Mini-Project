class BankAccount():
    def __init__(self,names,bal):
        self.name=names
        self.bal=bal

    def deposit(self,amt):
      if amt>0:
        self.bal+=amt
        print(f"Amount has been deposited. Current balance:{self.bal}")
      else:
        print("Enter a valdi integer!!")

    def withdraw(self,amt):
        if amt<self.bal:
            self.bal-=amt
            print(f"Amount has been withdrawn. Current balance:{self.bal}")
        else:
            print("Insufficient Balance!!")    
      
class SavingsAccount(BankAccount):
    def withdraw(self, amt):
      if amt<=self.bal and self.bal-amt>=100:
        self.bal-=amt
        print(f"Amount has been withdrawn. Current balance:{self.bal}")
      else:
        print("Transaction declined!! Account needs to have a minimum balance of 100")

if __name__== "__main__":
 names=input(print("Enter the name of the account holder:"))
 bal=int(input("Enter initial balance:"))

 if bal>0:
  account=BankAccount(names,bal)
 else:
  account=SavingsAccount(names,bal)

 ui=int(input("What would you like to do:\n1] Deposit\n2] Withdraw\n3] Exit"))
 if ui==1:
    amt=int(input("Enter amount to be deposited:"))
    account.deposit(amt)
 elif ui==2:
    amt=int(input("Enter amount to be withdrawn:"))
    account.withdraw(amt)
 elif ui==3:
    print("Exiting...\nThank You for Banking with us!!")
     
 else:
    print("Please enter valid input!!")