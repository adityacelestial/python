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

