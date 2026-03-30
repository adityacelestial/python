# Top K Frequent Elements 

# Problem Statement: 
# Return the k most frequent elements. 

# Input: 
# nums = [1,1,1,2,2,3], k = 2 

# Output: 
# [1,2] 

# Constraints: 

# 1 ≤ k ≤ len(nums) 

# Must be better than O(n log n) 

nums = [1,1,1,2,2,3] 
k = 2 

frequency={}

for num in nums:
    if num in frequency.keys():
        frequency[num]=frequency[num]+1
    else:
        frequency[num]=1
print(frequency)


maximumvalue=max(frequency.values())
output=[]
for i in range(2):
    
    for key in frequency.keys():
        if frequency[key]==maximumvalue:
            output.append(key)
     
    frequency.pop(output[-1])       
    maximumvalue=max(frequency.values())
    
print(output)



 