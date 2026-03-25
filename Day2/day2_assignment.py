# Q1. User Profile with Encapsulation 

# Topics: Encapsulation, Validation 

# Problem Statement: 

# Create a User class with private attributes: _username, _email, and _age. Provide getter and setter methods. The setter for email must validate that it contains '@' and '.' characters. The setter for age must ensure value is between 18 and 120. 

# Input: 

# user = User("alice", "alice@mail.com", 25) 

# user.set_email("invalid") 

# user.set_age(150) 

# print(user.get_email()) 

# print(user.get_age()) 

# Output: 

# ValueError: Invalid email format 

# ValueError: Age must be between 18 and 120 

# alice@mail.com 

# 25 

# Constraints: 

# Use private variables (prefix with _) 

# Raise ValueError with descriptive messages on invalid input 

# No direct attribute access allowed from outside the class 

class User:
    def __init__(self,username:str,email:str,age:int):
        self._username=username
        self._email=email
        self._age=age
    def get_email(self):
        return self._email
    def get_age(self):
        return self._age
    def set_email(self,email):
        try:
            
            if(email.find('@')!=-1 and email.find('.')!=-1):
                self._email=email
            else:
                raise ValueError("value error:Wrong email format")
        except ValueError as e:
            print(e)
    def set_age(self,age):
        try:
            if(age<18 or age>120):
                raise ValueError("Value Error:Invalid Age range")
            else:
                self._age=age
        except ValueError as e:
            print(e)
            
user = User("alice", "alice@mail.com", 25) 
user.set_email("invalid") 
user.set_age(150) 
print(user.get_email()) 
print(user.get_age()) 
        
        
        
        
# Q2. Inheritance — Admin and Customer Users 

# Topics: Inheritance, Polymorphism, super() 

# Problem Statement: 

# Create a base class User with attributes username and role, 
# and a method display_profile(). 
# Create two subclasses: AdminUser (extra attribute: permissions list)
# and CustomerUser (extra attribute: orders count). Override display_profile() 
# in both subclasses to include their specific data. 

# Input: 

# admin = AdminUser("admin1", ["manage_users", "view_logs"]) 

# customer = CustomerUser("cust1", 5) 

# admin.display_profile() 

# customer.display_profile() 

# Output: 

# Admin: admin1 | Permissions: manage_users, view_logs 

# Customer: cust1 | Orders: 5 

# Constraints: 

# Use super().__init__() to initialize base class 

# Override display_profile() in each subclass (Polymorphism) 

# Permissions must be a list of strings 

from typing import override
class User:
    def __init__(self,name,role):
        self.name=name
        self.role=role

class AdminUser(User):
    def __init__(self,name,role):
        super().__init__(name,role)
    
    def display_profile(self):
        print(f"Admin : {self.name} and roles :{self.role}")

class CustomerUser(User):
    def __init__(self,name,role):
        super().__init__(name,role)
    @override
    def display_profile(self):
        print(f"Customer {self.name} and count:{self.role}")

admin = AdminUser("admin1", ["manage_users", "view_logs"]) 

customer = CustomerUser("cust1", 5) 

admin.display_profile() 

customer.display_profile() 

# Q3. Composition — Order with Address and Payment 

# Topics: Composition, SRP 

# Problem Statement: 

# Build an Order class using composition.
# Create separate classes: Address (city, zip_code), PaymentInfo (method, amount), 
# and OrderItem (name, qty, price). The Order class should contain an Address, PaymentInfo,
# and a list of OrderItems. Implement order_summary() that returns the full breakdown. 

# Input: 

# addr = Address("Bangalore", "560001") 

# pay = PaymentInfo("UPI", 1500) 

# items = [OrderItem("Book", 2, 500), OrderItem("Pen", 5, 100)] 

# o = Order(addr, pay, items) rder

# order.order_summary() 

# Output: 

# Shipping: Bangalore - 560001 

# Items: Book x2 = 1000, Pen x5 = 500 

# Total: 1500 

# Payment: UPI 

# Constraints: 

# Do NOT use inheritance; use composition only 

# Each class must have a single responsibility 

# OrderItem total = qty * price 

class Address:
    def __init__(self,city,zipcode):
        self.city=city
        self.zipcode=zipcode

class PaymentInfo:
    def __init__(self,method,amount):
        self.method=method
        self.amount=amount
class OrderInfo:
    
    def __init__(self,name,qty,price):
        self.name=name
        self.qty=qty
        self.price=price


class Order:
    def __init__(self,address,payment,orders):
        self.address=address
        self.payment=payment
        self.orders=orders
    
    def order_summary(self):
        print(f"Shipping {self.address.city}-{self.address.zipcode}")
        print(f"items ",end="")
        total=0
        for item in self.orders:
            print(f"{item.name}x{item.qty}={item.qty*item.price}",end=" ")
            total+=item.qty*item.price
        print(f"\nTotal {self.payment.amount}")
        print(f"Method {self.payment.method}")
        
addr = Address("Bangalore", "560001") 

pay = PaymentInfo("UPI", 1500) 

items = [OrderInfo("Book", 2, 500), OrderInfo("Pen", 5, 100)] 

order = Order(addr, pay, items) 

order.order_summary() 


# section -2 SOLID principles


# Q4. SRP — Separate Validation, Storage, and Notification 

# Topics: SRP 

# Problem Statement: 

# You are given a monolithic UserService class that validates user data,
# saves to a JSON file, and sends a welcome message — all in one method.
# Refactor it into three SRP-compliant classes: UserValidator, UserStorage, and UserNotifier.
# Write an orchestrator function that uses all three. 

# Input: 

# data = {"username": "alice", "email": "alice@mail.com"} 

# register_user(data) 

# Output: 

# Validation passed 

# User saved to users.json 

# Welcome email sent to alice@mail.com 

# Constraints: 

# Each class must have exactly one reason to change 

# UserValidator raises ValueError on invalid data 

# UserStorage reads/writes JSON 

# UserNotifier prints the notification (simulated) 
import json
class UserValidation:
    def __init__(self,dict):
        self.dict=dict
        if(self.dict['username'].isalpha()):
            print("VAlidationpassed")

class UserStorage:
    def __init__(self,dict):
        self.dict=dict
        with open("user.json",'a') as file:
            json.dump(self.dict,file,indent=4)
        print("File stored in user.json")

class UserNotifier:
    def __init__(self,dict):
        self.dict=dict
        print(f"Email sent to {self.dict['email']}")
        
class register_user:
    def __init__(self,dict):
        validation=UserValidation(dict)
        storage=UserStorage(dict)
        notification=UserNotifier(dict)     
    
data = {"username": "alice", "email": "alice@mail.com"} 

register_user(data) 
    
    
# Q6. LSP — Fix the Bird Hierarchy 
# Topics: LSP, ISP, Abstraction 
# Problem Statement: 
# The following design violates LSP: 
# class Bird: def fly(self): ... 
# class Penguin(Bird): def fly(self): raise Exception("Can't fly") 
# Redesign the hierarchy so that no subclass breaks the contract of its parent. 
# Create proper abstract classes: Bird, FlyingBird, SwimmingBird. 
# Implement Sparrow, Eagle, Penguin, and Duck (Duck both flies and swims). 

# Input: 

# for bird in [Sparrow(), Eagle(), Penguin(), Duck()]: 

#     bird.move() 

class Bird(ABC):
    @abstractmethod
    def move():
        pass

class SwimmingBird(Bird):
    @abstractmethod
    def swim():
        pass
class FlyingBird(Bird):
    @abstractmethod
    def flying():
        pass
    
class Sparrow(FlyingBird):
    def flying():
        pass
class Eagle(FlyingBird):
    def flying():
        pass
class Penguin(Bird):
    def move():
        pass
class Duck(SwimmingBird):
    def swim():
        pass

# Output:
# Sparrow flies 
# Eagle flies 
# Penguin swims 
# Duck flies and swims 
# Constraints: 
# No method should raise an unexpected exception 
# Use abstract base classes with ABC 
# Duck must implement both flying and swimming interfaces 
# LSP: every subclass must be substitutable for its parent 





# Q7. DIP — Repository Pattern with Dependency Injection 

# Topics: DIP, Dependency Injection 

# Problem Statement: 

# Create a UserRepository abstract class with methods save(user) and find(username).
# Implement JSONUserRepository (stores in JSON file) and InMemoryUserRepository (stores in a dict).
# Create a UserService that depends on the abstraction, not the concrete class. Inject the repository at runtime. 

# Input: 

# repo = InMemoryUserRepository() 
# service = UserService(repo) 
# service.register({"username": "alice", "email": "a@b.com"}) 
# print(service.get_user("alice")) 

# Output: 
# {'username': 'alice', 'email': 'a@b.com'} 
# Constraints: 
# UserService constructor must accept UserRepository (abstraction) 
# Swapping InMemoryUserRepository with JSONUserRepository must not change UserService code 
# Use ABC for the repository interface 

from abc import ABC,abstractmethod

class UserRepo(ABC):
    
    @abstractmethod
    def save(content):
        pass
    
    @abstractmethod
    def find(content):
        pass

class Inmemorystorage(UserRepo):
    def __init__(self):
        self.data=[]

    def save(self,dict):
        self.data.append(dict)
        print(dict)
    
    def find(self,username):
        for i in self.data:
            if(i['username']==username):
                print(i)
                
        
class Jsonmemory(UserRepo):
    
    def __init__(self):
        pass
    
    def save(self,dict):
        with open("sample.json",'r') as file:
            data=json.load(file)
        data.append(dict)
        with open("sample.json",'w') as file:
            json.dump(data,file,indent=4)
    def find(self,username):
        
        with open("sample.json",'r') as file:
            data=json.load(file)
        for i in data:
            if i['username']==username:
                print(i)


class UserService:
    def __init__(self,repo):
        self.repo=repo
    
    def save(self,dict):
        self.repo.save(dict)
    
    def find(self,username):
        self.repo.find(username)
        
        
repo = Jsonmemory() 
service = UserService(repo) 
service.save({"username": "adityasai", "email": "aditya@b.com"}) 
print(service.find("adityasai")) 

# Q8. Thread vs Sequential — IO Simulation 

# Topics: Threading, IO-bound 

# Problem Statement: 

# Create a function fetch_data(source, delay) that simulates an API call using 
# time.sleep(delay). Run 5 calls sequentially and then using threading. 
# Print the total execution time for each approach. 

# Input: 

# sources = [("users", 2), ("orders", 3), ("products", 1), ("reviews", 2), ("inventory", 1)] 

# Output: 

# Sequential time: ~9.0s 

# Threaded time:   ~3.0s 

# Constraints: 

# Use threading.Thread or concurrent.futures.ThreadPoolExecutor 

# Print start and end log for each source 

# Measure time using time.time() 

import time
from datetime import datetime
start=datetime.now()
def fetch_data(dource,delay):
    time.sleep(delay)
sources = [("users", 2), ("orders", 3), ("products", 1), ("reviews", 2), ("inventory", 1)]

for source in sources:
    fetch_data(source[0],source[1])
    
print(f"sequential time needed {datetime.now()-start}")

import threading
thstart=datetime.now()
t1=threading.Thread(target=fetch_data,args=sources[0])
t1.start()
t2=threading.Thread(target=fetch_data,args=sources[1])
t2.start()
t3=threading.Thread(target=fetch_data,args=sources[2])
t3.start()
t4=threading.Thread(target=fetch_data,args=sources[3])
t4.start()
t5=threading.Thread(target=fetch_data,args=sources[4])
t5.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
print(f"Threading time {datetime.now()-thstart}")




# Q9. Race Condition — Shared Counter Fix 

# Topics: Race Condition, Thread Safety 

# Problem Statement: 

# Create a shared counter starting at 0. Spawn 10 threads, each incrementing the counter 1000 times. First demonstrate the race condition (incorrect final value), then fix it using threading.Lock. 

# Input: 

# # No explicit input — internal simulation 

# Output: 

# Without lock: 8743 (varies, often incorrect) 

# With lock:    10000 (always correct) 

# Constraints: 

# Run the unfixed version multiple times to show inconsistency 

# Use threading.Lock to fix 

# Do NOT use global keyword; pass lock and counter via a mutable container or class 

#part1 -withuot lock

import threading

class Counter:
    def __init__(self):
        self.counter=0
def increment():
    for _ in range(1000):
        counting.counter+=1
threads=[]
counting=Counter()
for t in range(10):
    thread=threading.Thread(target=increment,args=())
    thread.start()
    threads.append(thread)
for i in threads:
    i.join()
print(f"Without threading lock {counting.counter}")


counting2=Counter()
lock=threading.Lock()
def lockincrement():
    for _ in range(1000):
        with lock:
            counting.counter+=1


for t in range(10):
    thread=threading.Thread(target=lockincrement,args=())
    thread.start()
    threads.append(thread)
for i in threads:
    i.join()
print(f"Thread locking {counting2.counter}")




# Q10. Multiprocessing — CPU-bound Speedup 

# Topics: Multiprocessing, CPU-bound 

# Problem Statement: 

# Write a function compute_squares(n) that computes the sum of squares from 1 to n.
# Run it for 4 large values sequentially and then using multiprocessing.Pool. Compare execution times. 

# Input: 

# values = [10_000_000, 20_000_000, 15_000_000, 25_000_000] 

# Output: 

# Sequential time: ~X.Xs 

# Multiprocessing time: ~Y.Ys (faster) 

# Constraints: 

# Use multiprocessing.Pool.map() 

# Measure wall-clock time with time.time() 

# Print individual results for verification 

# in separate file




# Q11. Async IO — Concurrent API Simulation 

# Topics: Async, Event Loop, Coroutines 

# Problem Statement: 

# Convert synchronous API-call simulation into async using asyncio.
# Create async fetch(url, delay) that uses await asyncio.sleep(delay). Use asyncio.gather() to run 4 calls concurrently.
# Compare total time vs sync version. 

# Input: 

# urls = [("api/users", 2), ("api/orders", 3), ("api/products", 1), ("api/reviews", 2)] 

# Output: 

# Sync time:  ~8.0s 

# Async time: ~3.0s 

# Constraints: 

# Use async def and await 

# Use asyncio.gather() to run tasks concurrently 

# Print each task's start and completion timestamp 

from datetime import datetime
import asyncio
import time
seqstart=datetime.now()

urls = [("api/users", 2), ("api/orders", 3), ("api/products", 1), ("api/reviews", 2)] 

def fetch(url,t):
    time.sleep(t)

for url in urls:
    fetch(url[0],url[1])

print(f"Without async {datetime.now()-seqstart}")


astart=datetime.now()
async def afetch(url,t):
    await asyncio.sleep(t)
    
async def demonstrate():
    await asyncio.gather(*(afetch(url,t) for (url,t) in urls))

asyncio.run(demonstrate()) 

print(f"Asyncronous execution {datetime.now()-astart}")


# Section D-- FastAPI and Pydantic


# Q12. Pydantic — User Schema with Nested Validation 

# Topics: Pydantic, Nested Models, Validation 

# Problem Statement: 

# Create Pydantic models: Address (street, city, zip_code), UserCreate (username, email, password, age, address).
# Add validations: email must contain '@', password min 8 chars, age 18-120, zip_code must be exactly 6 digits.
# Create UserResponse that excludes password. 

# Input: 

# data = {"username": "alice", "email": "alice@mail.com", 

#   "password": "securepass", "age": 25, 

#   "address": {"street": "MG Road", "city": "Bangalore", "zip_code": "560001"}} 

# user = UserCreate(**data) 

# print(UserResponse(**user.model_dump())) 

# Output: 

# username='alice' email='alice@mail.com' age=25 address=Address(...) 

# Constraints: 

# Use field_validator or Field() constraints 

# Invalid data must raise ValidationError with clear messages 

# UserResponse must NOT include password field 

# Use model_dump() for serialization 

from pydantic import BaseModel,Field,field_validator
from typing import Optional

class Address(BaseModel):
    street:str
    city:str
    zipcode:str =Field(...,pattern="^\d{6}$")

class UserCreate(BaseModel):
    username:str
    email:str
    password:str=Field(min_length=8)
    age:int=Field(ge=18,le=120)
    address:Address
    
    @field_validator("email")
    def validate_email(cls,v):
        if "@" not in v:
            raise ValueError("Email must contain @")
        return v

class UserResponse(BaseModel):
    username:str
    email:str
    age:int
    address:Address

data = {
    "username": "alice",
    "email": "alice@mail.com",
    "password": "securepass",
    "age": 25,
    "address": {
        "street": "MG Road",
        "city": "Bangalore",
        "zipcode": "560001"
    }
}

user = UserCreate(**data)

print(UserResponse(**user.model_dump()))





# Q13. FastAPI — Health Check and CRUD Endpoints 

# Topics: FastAPI, Pydantic, REST, HTTP Methods 

# Problem Statement: 

# Create a FastAPI application with the following endpoints for a 
# Task resource (store tasks in a Python list in memory): 

# GET /health — returns {"status": "healthy"} 

# POST /tasks — create a new task 

# GET /tasks — list all tasks with optional ?status= filter 

# GET /tasks/{task_id} — get task by ID 

# PUT /tasks/{task_id} — update a task 

# DELETE /tasks/{task_id} — delete a task 

# Input: 

# # POST /tasks 

# {"title": "Write report", "description": "Q2 summary", "status": "pending"} 

 

# # GET /tasks?status=pending 

# Output: 

# # POST response (201) 

# {"id": 1, "title": "Write report", "description": "Q2 summary", "status": "pending"} 

 

# # GET response (200) 

# [{"id": 1, "title": "Write report", ...}] 

# Constraints: 

# Use Pydantic models: TaskCreate, TaskUpdate, TaskResponse 

# Task ID must be auto-generated (incrementing integer) 

# Status must be one of: pending, in_progress, completed 

# Return 404 if task not found 

# Return 201 on successful creation 

# Test all endpoints via Postman 




# Section E

# Q18. Filter and Transform with Comprehension 

# Topics: Dictionary Comprehension 

# Problem Statement: 

# Given a list of user dictionaries, use a single dictionary comprehension to create a mapping of username → email for users who are active and aged 18+. 

# Input: 

# users = [ 

#   {"username": "alice", "email": "a@b.com", "age": 25, "active": True}, 

#   {"username": "bob", "email": "b@b.com", "age": 17, "active": True}, 

#   {"username": "carol", "email": "c@b.com", "age": 30, "active": False}, 

#   {"username": "dave", "email": "d@b.com", "age": 22, "active": True}, 

# ] 

# Output: 

# {'alice': 'a@b.com', 'dave': 'd@b.com'} 

# Constraints: 

# Use a single dictionary comprehension (one line) 

# Both conditions (active AND age >= 18) must be met 

users = [ 

  {"username": "alice", "email": "a@b.com", "age": 25, "active": True}, 

  {"username": "bob", "email": "b@b.com", "age": 17, "active": True}, 

  {"username": "carol", "email": "c@b.com", "age": 30, "active": False}, 

  {"username": "dave", "email": "d@b.com", "age": 22, "active": True}, 

] 

result = {u["username"]: u["email"] for u in users if u["active"] and u["age"] >= 18}
print(result)





# Q19. Flatten and Deduplicate Tags 

# Topics: List Comprehension, Sets 

# Problem Statement: 

# Given a list of articles (each with a list of tags), extract all unique tags sorted alphabetically using comprehensions and sets. 

# Input: 

articles = [ 

  {"title": "AI Intro", "tags": ["python", "ml", "ai"]}, 

  {"title": "Web Dev", "tags": ["python", "fastapi", "api"]}, 

  {"title": "Data 101", "tags": ["ml", "pandas", "python"]}, 

] 

# Output: 

# ['ai', 'api', 'fastapi', 'ml', 'pandas', 'python'] 

# Constraints: 

# Use set comprehension or list comprehension with set conversion 

# Output must be sorted alphabetically 

# Solve in no more than 2 lines of code 

unique_tags = {tag for article in articles for tag in article["tags"]}
result = sorted(unique_tags)


# Q20. Map HTTP Status Codes to Categories 

# Topics: List Comprehension, HTTP Status Codes 

# Problem Statement: 

# Given a list of HTTP response codes, use a list comprehension to classify each as success, client_error, or server_error. 

# Input: 

codes = [200, 201, 404, 500, 301, 403, 502, 204] 

# Output: 

# [(200, 'success'), (201, 'success'), (404, 'client_error'), 

#  (500, 'server_error'), (301, 'redirect'), (403, 'client_error'), 

#  (502, 'server_error'), (204, 'success')] 

# Constraints: 

# 2xx → success, 3xx → redirect, 4xx → client_error, 5xx → server_error 

# Use a single list comprehension with a helper function or inline conditional 
result = [
    (c,
     "success" if 200 <= c < 300 else
     "redirect" if 300 <= c < 400 else
     "client_error" if 400 <= c < 500 else
     "server_error" if 500 <= c < 600 else
     "other")
    for c in codes
]