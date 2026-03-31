"""
    Problem Statement: 
Given a list of integers, remove duplicate elements while preserving the original order of first occurrence. 

Input Format: 
A list of integers nums 

Input: 
nums = [1, 2, 2, 3, 4, 4, 5] 

Output Format: 
A list of integers 

Output: 
[1, 2, 3, 4, 5] 

Constraints: 

1 ≤ len(nums) ≤ 10^5 

Elements can be any integers 

Do not use set() 

Time Complexity: O(n) 
"""

nums = [1, 2, 2, 3, 4, 4, 5] 

output=[]

for num in nums:
    if num in output:
        continue
    else:
        output.append(num)

# first question output:
print(output)

