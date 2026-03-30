# Environment Variables Loader 

# Problem Statement: 
# Read variables from .env file and load into program. 

# Input (.env): 

# DB_HOST=localhost 
# DB_PORT=5432 

# Output: 
# {'DB_HOST':'localhost','DB_PORT':'5432'} 

from dotenv import dotenv_values

env=dotenv_values('.env')
print(env)
print(dict(env))


