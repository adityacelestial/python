"""
    Problem Statement: 
Given a list of integers, remove duplicate elements while preserving the original order of first occurrence. 

Input Format: 
A list of integers nums 

Input: 
nums = [1, 2, 2, 3, 4, 4, 5] 

Output Format: 
A list of integers 

Output: 
[1, 2, 3, 4, 5] 

Constraints: 

1 ≤ len(nums) ≤ 10^5 

Elements can be any integers 

Do not use set() 

Time Complexity: O(n) 
"""

nums = [1, 2, 2, 3, 4, 4, 5] 

output=[]

for num in nums:
    if num in output:
        continue
    else:
        output.append(num)

# first question output:
print(output)

"""
    Second Largest Unique Element 

Problem Statement: 
Find the second largest unique number in the list. 

Input: 
nums = [10, 20, 4, 45, 99, 99] 

Output: 
45 

Constraints: 

2 ≤ len(nums) ≤ 10^5 

Must ignore duplicates 

Do not use sorting 

O(n) time 
    
"""

# to find the second largest element from the list

nums = [10, 20, 4, 45, 99, 99] 
maximum=max(nums)
secondmin=0
for num in nums:
    if num<maximum and num>secondmin:
        secondmin=num
    else:
        continue
print(secondmin)



"""
    Group Anagrams 

Problem Statement: 
Group strings that are anagrams of each other. 

Input: 
words = ["eat","tea","tan","ate","nat","bat"] 

Output: 
[["eat","tea","ate"],["tan","nat"],["bat"]] 

Constraints: 

1 ≤ len(words) ≤ 10^4 

Each word length ≤ 100 

Time Complexity: O(n * k log k) 
"""
from collections import defaultdict

def groupAnagrams(words):
    groups = defaultdict(list)

    for word in words:
        key = ''.join(sorted(word)) 
        groups[key].append(word)

    return list(groups.values())


words = ["eat","tea","tan","ate","nat","bat"]
print(groupAnagrams(words))


    
    
    
# Top K Frequent Elements 

# Problem Statement: 
# Return the k most frequent elements. 

# Input: 
# nums = [1,1,1,2,2,3], k = 2 

# Output: 
# [1,2] 

# Constraints: 

# 1 ≤ k ≤ len(nums) 

# Must be better than O(n log n) 

nums = [1,1,1,2,2,3] 
k = 2 

frequency={}

for num in nums:
    if num in frequency.keys():
        frequency[num]=frequency[num]+1
    else:
        frequency[num]=1
print(frequency)


maximumvalue=max(frequency.values())
output=[]
for i in range(2):
    
    for key in frequency.keys():
        if frequency[key]==maximumvalue:
            output.append(key)
     
    frequency.pop(output[-1])       
    maximumvalue=max(frequency.values())
    
print(output)


# Word Frequency Counter (File Handling) 

# Problem Statement: 
# Read a .txt file and count frequency of each word. 

# Input (file content): 

# hello world 
# hello python 

# Output: 
# {'hello':2,'world':1,'python':1} 

# Constraints: 

# Case insensitive 

# Ignore punctuation 

# File size ≤ 10MB 

import re


wordfreq={}

    
# with open('sampletext.txt','r') as f:
#     for i in f.readlines():
#         words=i.split(" ")
#         for word in words:
#             word=word.replace("\n","")
#             if word in wordfreq:
#                 wordfreq[word]+=1
#             else:
#                 wordfreq[word]=1       

# print(wordfreq)


# JSON Validation 

# Problem Statement: 
# Check if a string is a valid JSON. 

# Input: 
# '{"name": "John", "age": 30}' 

# Output: 
# True 

# Input: 
# '{"name": "John", "age": }' 

# we have to use the json library for this use case

import json

# jsonstring='{"name": "John", "age": 30}'
jsonstring='{"name": "John", "age": }' 

try:
    jsonload1=json.loads(jsonstring)
    print('Valid JSON')
except json.JSONDecodeError as e:
    print(f"Invalid JSON:{e}")
    
    
# custom exceptions

# Custom Exception Handling 

# Problem Statement: 
# Raise a custom exception if salary < 10000. 

# Input: 
# salary = 8000 

# Output: 
# "SalaryTooLowError" 

class LowSalaryException(Exception):
    def __init__(self,message="salary too low"):
        self.message=message
    
        super().__init__(self.message)
        
salary=8000

try:
    if salary>10000:
        print("Good salary")
    else:
        raise LowSalaryException()
except LowSalaryException as e:
    print(e)
    
"""
        Flatten Nested List (Recursive) 

Problem Statement: 
Flatten a nested list of arbitrary depth. 

Input: 
[1,[2,[3,4],5],6] 

Output: 
[1,2,3,4,5,6] 

Constraints: 

Depth ≤ 1000 

Use recursion 
        
        """

global unpackedlist
unpackedlist=[]
def listunpacking(packedlist):
    # we use the isinstance to compare the types
    for item in packedlist:
        if isinstance(item,list):
            listunpacking(item)
        else:
            unpackedlist.append(item)

packed=[1,[2,[3,4],5],6] 

listunpacking(packed)
print(unpackedlist)

# Lambda + Sorting Complex Structure 

# Problem Statement: 
# Sort list of dictionaries by age. 

# Input: 
# [{'name':'A','age':30},{'name':'B','age':20}] 

# Output: 
# [{'name':'B','age':20},{'name':'A','age':30}] 


# sorting dictionaries according to the age

# dictionaries=[{'name':'A','age':30},{'name':'B','age':20}] 
dictionaries=[{'name':'B','age':20},{'name':'A','age':30}] 

sorteddict=sorted(dictionaries,key=lambda a:a['age'])
print(sorteddict)

# Environment Variables Loader 

# Problem Statement: 
# Read variables from .env file and load into program. 

# Input (.env): 

# DB_HOST=localhost 
# DB_PORT=5432 

# Output: 
# {'DB_HOST':'localhost','DB_PORT':'5432'} 

from dotenv import dotenv_values

env=dotenv_values('.env')
print(env)
print(dict(env))


# Logging System 

# Problem Statement: 
# Log errors with timestamp to file (txt or Json). 

# Output Format: 

# 2026-01-01 10:00:00 ERROR Something failed 

# explain the above

from datetime import datetime
def logerror(message="ERROR something failed\n"):
    
    timestamp=datetime.now().strftime("%y-%m-%d %H:%M:%S")
    
    with open("log.txt",'a') as f:
        f.write(f"{timestamp} {message}")
    print(timestamp)
    

logerror()
logerror("Main system DOWN!\n")
logerror("Illegal Access\n")

# Create Dictionary from Two Lists 

# Problem Statement: 
# Given two lists, create a dictionary mapping keys to values. 

# Input: 
# keys = ['a','b','c'] 
# values = [1,2,3] 

# Output: 
# {'a':1,'b':2,'c':3} 

# Constraints: 

# Use dictionary comprehension 

keys = ['a','b','c'] 
values = [1,2,3] 

dictionary={keys[it]:values[it] for it in range(len(keys))}
print(dictionary)



# Invert Dictionary Using Comprehension 

# Input: 
# {'a':1,'b':2,'c':3} 

# Output: 
# {1:'a',2:'b',3:'c'} 

# Constraints: 

# Keys are unique 

dictionary={'a':1,'b':2,'c':3} 
reverseddict={value:key for key,value in dictionary.items()}

print(reverseddict)


# Extract Words Starting with Vowel 

# Input: 
# "apple banana orange grape" 

# Output: 
# ["apple","orange"] 

# Constraints: 

# Case insensitive 

# Use List Comprehension 

vowels=['a','e','i','o','u']
strings="apple banana orange grape" 
stringlist=strings.split(" ")
print(stringlist)
outputlist=[item for item in stringlist if item[0] in vowels]
print(outputlist)

# Replace Negative Numbers with 0 

# Input: 
# [1,-2,3,-4,5] 

# Output: 
# [1,0,3,0,5] 

# Constraints: 

# Use List Comprehension 


samplelist=[1,-2,3,-4,5] 

outputlist=[num if num>0 else 0 for num in samplelist]
print(outputlist)

# Multi-condition List Comprehension 

# Problem Statement: 
# Return numbers divisible by both 2 and 3. 

# Input: 
# range(1,20) 

# Output: 
# [6,12,18] 

multidiv=[num  for num in range(1,20) if num%2==0 and num%3==0]

print(multidiv)



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







 
# Problem 

# Fix this design: 

# class Bird: 
#    def fly(self): 
#        pass 
 
# class Penguin(Bird): 
#    def fly(self): 
#        raise Exception("Cannot fly") 
# Task 

# Redesign system so: 

# No subclass breaks behavior 

# LSP is followed 

class Bird:
    def eat(self):
        print("Eating...")


class FlyingBird(Bird):
    def fly(self):
        print("Flying...")


class Sparrow(FlyingBird):
    pass


class Penguin(Bird):
    def swim(self):
        print("Swimming...")





#Q20
# E-Commerce Checkout System (ALL SOLID + OOP) 

# Problem 

# Design checkout system with: 

# Multiple payment methods (UPI, Card) 

# Discount system (Festival, Premium user) 

# Logging 


# Input 

# checkout = Checkout(payment=UPI(), discount=FestivalDiscount()) 
# checkout.process(1000) 

 

# Output 

# Final Amount: 900 
# Payment Successful via UPI 
 

# Requirements 

# Plug-and-play: 

# Add new payment methods 

# Add new discount strategies 


# Constraints 

# Must follow: 

# SRP → separate classes 

# OCP → extend without modifying 

# LSP → interchangeable behaviors 

# ISP → small interfaces 

# DIP → depend on abstraction 


from abc import ABC,abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self,amount):
        pass
class Discount(ABC):
    @abstractmethod
    def apply(self,amount):
        pass

class Logger(ABC):
    def log(self,message):
        pass

class Upi(Payment):
    def pay(self,amount):
        self.type="upi"
        print(f"The payment of {amount} was made through UPI")

class Card(Payment):
    def pay(self,amount):
        self.type='card'
        print(f"The amount {amount} was paid using card")

class PremiumCustomer(Discount):
    def apply(self,amount):
        return amount*0.9
class FestivalOffer(Discount):
    def apply(self,amount):
        return amount*0.8
    
class PaymentLogger(Logger):
    def log(self,type,amount):
        with open("shoppinglog.txt",'a') as f:
            f.write(f"The amount {amount} was paid using {type}")
            

class Checkout:
    def __init__(self,payment:Payment,discount:Discount,logger:Logger):
        self.payment=payment
        self.discount=discount
        self.logger=logger
    
    def process(me,amount):
        me.payment.pay(amount)
        amountpaid=me.discount.apply(amount)
        print(amountpaid)
        me.logger.log(me.payment.type,amountpaid)
        
checkout=Checkout(payment=Upi(),discount=FestivalOffer(),logger=PaymentLogger())
checkout.process(1000)





# CLI-Based User Management System  

# Objective 

# Build a CLI-based User Management System using Python that: 

# Stores user data in a JSON file 

# Performs core user operations (CRUD-like) 

# Implements logging for all system activities 

# Follows clean code structure and error handling practices 

# Project Structure 

# user_management/ 
# │── main.py 
# │── utils.py 
# │── storage.py 
# │── logger.py 
# │── users.json 
# │── logs.txt 
 

# Data Storage (users.json) 

# { 
#  "users": [] 
# } 
 
 
 