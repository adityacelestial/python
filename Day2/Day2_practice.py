# Topic -1 OOP Fundamentals
# 1• Create a User class with private attributes and getter/setter methods 

class User:
    def setusername(self,username):
        self.__username=username
    
    def setuserage(self,age):
        self.__age=age
    
    def getname(self):
        print(self.__username)
    def getage(self):
        print(self.__age)

sampleuser=User()

sampleuser.setusername("Aditya")
sampleuser.setuserage(22)

sampleuser.getname()
sampleuser.getage()


# 2• Implement inheritance with AdminUser and CustomerUser classes 

class AdminUser:
    def __init__(self,type):
        pass


# 3• Implement method overriding for display_profile() 
from typing import override

class AdminUser:
    def __init__(self):
        print("Admin user was initiated")
    def display_profile(self):
        print("This is a admin user")

class CustomerUser:
    def __init__(self):
        print("customer was initiated")
    @override
    def display_profile(self):
        print("this is a customer type")
        

admin=AdminUser()
customer=CustomerUser()

admin.display_profile()
customer.display_profile()


# 4• Build a composition-based Order class that contains Address and PaymentInfo

class Address:
    def __init__(self,line1,area,city):
        self.line1=line1
        self.area=area
        self.city=city

class Payment:
    def __init__(self,type):
        self.type=type
        

class Order:
    def __init__(self,order_id,address,payment):
        self.order_id=order_id
        self.address=address
        self.payment=payment
    def printdetails(self):
        print(self.address.area)
        print(self.payment.type)
        
address=Address("line1","nallapadu","guntur")
payment=Payment("UPI")

order=Order(1,address,payment)

order.printdetails()

# Multi-threading,multi processing etc

#• 5.Create a script that runs two IO-bound tasks using threads 
import threading
import time

def io_task(name):
    print(f"{name} started")
    time.sleep(2)
    print(f"{name} finished")
start=time.time()

t1=threading.Thread(target=io_task,args=("Task_!",))
t2=threading.Thread(target=io_task,args=("Task2",))

t1.start()
t2.start()
t1.join()
t2.join()
print(f"Threaded time {time.time()-start}")
# •6. Create a script that runs two CPU-bound tasks using multiprocessing
from multiprocessing import Process
import time

def cpu_task(name):
    
    print(f"Process {name} started")
    
    total=0
    for i in range(10**4):
        total+=i
    
    print(f"Process {name} finished")
if __name__=="__main__":
    
    p1=Process(target=cpu_task,args=("Task1",))
    p2=Process(target=cpu_task,args=("Task_2",))
    start=time.time()
    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(f"Total time taken{time.time()-start}")
# • 7.Demonstrate race condition with shared counter and fix it using a lock 

# • 8.Compare runtime for sequential vs threaded vs multiprocessing execution

