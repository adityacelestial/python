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
    

 