# Q3. Raw SQL with psycopg2 — Connect to Supabase & Query

# Topics: psycopg2, Database Connection, Raw SQL, Environment Variables

# Problem Statement:

# Connect to your Supabase PostgreSQL database using psycopg2 and the connection URL stored in your .env file. 
# Write a script that: (a) connects to the database, (b) runs SELECT * FROM users LIMIT 5;
# on your existing Day-2 users table, (c) prints each row, and (d) properly closes the connection.
# Handle the case where the table might not exist.

# Input:


# # .env file contains:

# # DATABASE_URL=postgresql://postgres:<password>@<host>:5432/postgres


# run_raw_query()


# Output:


# Connected to Supabase successfully!


# Users (raw SQL):

# (1, 'alice', 'alice@mail.com', 'hashed_pw', '2026-03-20T09:00:00')

# (2, 'bob', 'bob@mail.com', 'hashed_pw', '2026-03-20T09:05:00')


# Rows fetched: 2

# Connection closed.


# Constraints:

# • Load DATABASE_URL from .env using python-dotenv

# • Use psycopg2.connect() with the connection string

# • Use parameterized queries (no string concatenation)

# • Wrap in try/except/finally — always close the connection

# • Handle psycopg2.errors.UndefinedTable if table doesn’t exist

# • Print meaningful error messages on failure

import psycopg2
from dotenv import load_dotenv
import os
# conn=psycopg2.connect(
#     host='localhost',
#     dbname="dvd",
#     user='postgres',
#     password='1978',
    
#     port=5432
# )
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cur=conn.cursor()

cur.execute("""
    SELECT * from employees
""")
print(cur.fetchall())

cur.close()
conn.close()





