# Q20. Map HTTP Status Codes to Categories 

# Topics: List Comprehension, HTTP Status Codes 

# Problem Statement: 

# Given a list of HTTP response codes, use a list comprehension to classify each as success, client_error, or server_error. 

# Input: 

codes = [200, 201, 404, 500, 301, 403, 502, 204] 

# Output: 

# [(200, 'success'), (201, 'success'), (404, 'client_error'), 

#  (500, 'server_error'), (301, 'redirect'), (403, 'client_error'), 

#  (502, 'server_error'), (204, 'success')] 

# Constraints: 

# 2xx → success, 3xx → redirect, 4xx → client_error, 5xx → server_error 

# Use a single list comprehension with a helper function or inline conditional 
result = [
    (c,
     "success" if 200 <= c < 300 else
     "redirect" if 300 <= c < 400 else
     "client_error" if 400 <= c < 500 else
     "server_error" if 500 <= c < 600 else
     "other")
    for c in codes
]