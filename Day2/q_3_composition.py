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


