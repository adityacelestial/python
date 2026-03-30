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



 