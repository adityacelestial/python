# Replace Negative Numbers with 0 

# Input: 
# [1,-2,3,-4,5] 

# Output: 
# [1,0,3,0,5] 

# Constraints: 

# Use List Comprehension 


samplelist=[1,-2,3,-4,5] 

outputlist=[num if num>0 else 0 for num in samplelist]
print(outputlist)

