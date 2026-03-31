

# Section C — SQLAlchemy ORM

# Q4. SQLAlchemy Setup — Engine, Session & Connection Verification

# Topics: SQLAlchemy Engine, Session, create_engine, sessionmaker, Environment Variables

# Problem Statement:

# Create a database.py module that sets up SQLAlchemy to connect to your Supabase PostgreSQL.
# Define the engine using the DATABASE_URL from .env, create a session factory using sessionmaker, 
# and define a Base using declarative_base(). Write a function verify_connection() that executes SELECT 1 to confirm the connection works.

# Input:

# from database import engine, SessionLocal, verify_connection

# verify_connection()

# Output:

# Engine created: postgresql://postgres:***@<host>:5432/postgres

# Session factory ready.

# Connection verified: SELECT 1 returned 1

# Database connection successful!


# Constraints:

# • Load DATABASE_URL from .env file

# • Use create_engine() with echo=False

# • Use sessionmaker(autocommit=False, autoflush=False, bind=engine)

# • verify_connection() must use engine.connect() and execute raw SQL

# • Mask the password when printing the engine URL

# • Handle connection failure with a clear error message

from dotenv import load_dotenv
import os
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker,declarative_base

load_dotenv()

DATABASE_URL=os.getenv('DATABASE_URL')


def mask_password(url: str) -> str:
    if "://" not in url:
        return url
    before, after = url.split("://", 1)
    user_pass, host = after.split("@", 1)

    if ":" in user_pass:
        username, _password = user_pass.split(":", 1)
        return f"{before}://{username}:***@{host}"

    return url  


engine=create_engine(DATABASE_URL,echo=False,future=True)

print(f"Database created {mask_password(DATABASE_URL)}")

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

base=declarative_base()

with engine.connect() as conn:
    result=conn.execute(text("SELECT 1")).scalar()
    print(result)
    
