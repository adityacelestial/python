# JSON Validation 

# Problem Statement: 
# Check if a string is a valid JSON. 

# Input: 
# '{"name": "John", "age": 30}' 

# Output: 
# True 

# Input: 
# '{"name": "John", "age": }' 

# we have to use the json library for this use case

import json

# jsonstring='{"name": "John", "age": 30}'
jsonstring='{"name": "John", "age": }' 

try:
    jsonload1=json.loads(jsonstring)
    print('Valid JSON')
except json.JSONDecodeError as e:
    print(f"Invalid JSON:{e}")
    
    
