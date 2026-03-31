#Question-2:

# Q2. @retry Decorator with Max Attempts

# Topics: Decorators with Arguments, Exception Handling, Closures

# Problem Statement:

# Write a parameterized decorator @retry(max_attempts) that retries a function up to max_attempts times
# if it raises an exception. After each failed attempt, print the attempt number and the error.
# If all attempts fail, raise the last exception. Apply it to a function fetch_data() 
# that simulates a flaky API call using random.choice.

# Input:

# import random

# random.seed(42) # For reproducible output

# @retry(max_attempts=5)

# def fetch_data():

# """Simulates a flaky API call."""

# if random.choice([True, False]):

# raise ConnectionError("Server unreachable")

# return {"status": "ok", "data": [1, 2, 3]}

# result = fetch_data()

# print(f"Result: {result}")

# Output:

# [retry] Attempt 1 failed: Server unreachable

# [retry] Attempt 2 succeeded!

# Result: {'status': 'ok', 'data': [1, 2, 3]}


# Constraints:

# • Decorator must accept max_attempts as a parameter

# • Print each failed attempt with attempt number and error message

# • Print success message with the attempt number that succeeded

# • If all attempts fail, raise the original exception with message: "All {max_attempts} attempts failed"

# • Use functools.wraps to preserve function metadata

from functools import wraps
import random
def retry(max_attempts):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            for i in range(max_attempts):
                try:
                    output=func()
                    print(f"[retry] Attempt {i+1} succeded")
                    print(output)
                    break
                except ConnectionError as e:
                    print(f"[retry] Attempt {i+1} and {e}")
        return wrapper
    return decorator
                



random.seed(42) # For reproducible output
@retry(max_attempts=5)
def fetch_data():
    if random.choice([True, False]):
        raise ConnectionError("Server unreachable")
    return {"status": "ok", "data": [1, 2, 3]}


result = fetch_data()

print(f"Result: {result}")



