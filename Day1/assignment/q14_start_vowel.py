# Extract Words Starting with Vowel 

# Input: 
# "apple banana orange grape" 

# Output: 
# ["apple","orange"] 

# Constraints: 

# Case insensitive 

# Use List Comprehension 

vowels=['a','e','i','o','u']
strings="apple banana orange grape" 
stringlist=strings.split(" ")
print(stringlist)
outputlist=[item for item in stringlist if item[0] in vowels]
print(outputlist)

