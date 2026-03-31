"""
    Second Largest Unique Element 

Problem Statement: 
Find the second largest unique number in the list. 

Input: 
nums = [10, 20, 4, 45, 99, 99] 

Output: 
45 

Constraints: 

2 ≤ len(nums) ≤ 10^5 

Must ignore duplicates 

Do not use sorting 

O(n) time 
    
"""

# to find the second largest element from the list

nums = [10, 20, 4, 45, 99, 99] 
maximum=max(nums)
secondmin=0
for num in nums:
    if num<maximum and num>secondmin:
        secondmin=num
    else:
        continue
print(secondmin)



