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



