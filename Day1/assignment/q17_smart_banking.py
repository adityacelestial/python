# Smart Banking System (OOP + SRP + Encapsulation) 

# Problem 

# Design a banking system with: 

# Deposit 

# Withdraw 

# Balance check 

 

# Input 

# acc = SavingsAccount("John", 1000) 
# acc.deposit(500) 
# acc.withdraw(200) 
# acc.get_balance() 

 

# Output 

# Balance: 1300 

# SRP means Single responsibility principle
# Requirements 

# Use private variables (encapsulation) 

# Create separate classes: 

# Account 

# Transaction Logger (SRP) 

# Constraints 

# No direct balance access 

# Add validation (no negative withdraw) 

from datetime import datetime
class TransactionLogger:
    def log_deposit(self,deposit,balence):
        with open("transactionlog.txt",'a') as f:
            f.write(f"Deposit:{deposit} Balence:{balence} Timestamp :{datetime.now()}\n")
    def log_withdraw(self,withdraw,balence):
        with open("transactionlog.txt",'a') as f:
            f.write(f"withdraw:{withdraw} Balence:{balence} Timestamp :{datetime.now()}\n")
    def log_balence_check(self,balence):
        with open("transactionlog.txt",'a') as f:
            f.write(f"Balence_check  Balence{balence} Timestamp: {datetime.now()}\n")
        

class SavingAccount(TransactionLogger):
    def __init__(self,name,initialbalence):
        self.__name=name
        self.__balence=initialbalence
        
    def deposit(self,money):
        self.__balence=self.__balence+money
        super().log_deposit(money,self.__balence)
    
    def withdraw(self,money):
        if(self.__balence-money>0):
            
            self.__balence=self.__balence-money
            
            super().log_withdraw(money,self.__balence)
        else:
            print("Insufficient Balence")
    
    def get_balence(self):
        
        print(f"Balence is {self.__balence}")
        super().log_balence_check(self.__balence)

acc=SavingAccount('Adithya',1000)
acc.deposit(500)
acc.withdraw(200)
acc.get_balence()







 