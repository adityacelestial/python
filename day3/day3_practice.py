# Decorator 
# Decorators in python will act like a wrapper 
# Decorator will add some additional behavious into the function with out modifying the additional code 
# in the function

def my_decorator(fun):
    def wrapper():
        print("Before function run")
        print("After function run")
        fun()
        
    return wrapper


@my_decorator
def hello_func():
    print("Hello function in the wrapper")
    

hello_func()


#wraps in application

def greet():
    print("Hello")

print(greet.__name__)
print(greet.__doc__)
print(greet)

def my_decorator(func):
    def wrapper():
        print("First task")
        func()
        print("Last task")
    return wrapper

@my_decorator
def greeting():
    print("Greetings to you")

greeting()


# wraps in python

# arguments in decorators

from functools import wraps


