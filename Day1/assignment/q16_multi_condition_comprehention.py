# Multi-condition List Comprehension 

# Problem Statement: 
# Return numbers divisible by both 2 and 3. 

# Input: 
# range(1,20) 

# Output: 
# [6,12,18] 

multidiv=[num  for num in range(1,20) if num%2==0 and num%3==0]

print(multidiv)



