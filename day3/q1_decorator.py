#Question-1:


# Problem Statement:

# Write a decorator @timer that measures and prints the execution time of any function it decorates. 
# The decorator must preserve the original function’s name and docstring using functools.wraps.
# Apply it to a function compute_squares(n) that computes the sum of squares from 1 to n.

# Input:


# @timer

# def compute_squares(n):

# """Computes sum of squares from 1 to n."""

# return sum(i * i for i in range(1, n + 1))


# result = compute_squares(1_000_000)

# print(f"Result: {result}")

# print(f"Function name: {compute_squares.__name__}")

# print(f"Docstring: {compute_squares.__doc__}")


# Output:


# [timer] compute_squares executed in 0.0823s

# Result: 333333833333500000

# Function name: compute_squares

# Docstring: Computes sum of squares from 1 to n.


# Constraints:

# • Use functools.wraps to preserve function metadata

# • Time must be printed in seconds rounded to 4 decimal places

# • Format: [timer] <function_name> executed in <time>s

# • Decorator must work on any function with any number of argument

from functools import wraps
from datetime import datetime

def timer(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start=datetime.now()
        result=func(*args,**kwargs)
        print(result)
        print(f"The time taken is {datetime.now()-start}")
    return wrapper
        

@timer
def compute_squares(n):
    """Computes sum of squares from 1 to n."""
    return sum(i * i for i in range(1, n + 1))

compute_squares(100000)

