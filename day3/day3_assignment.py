#Question-1:


# Problem Statement:

# Write a decorator @timer that measures and prints the execution time of any function it decorates. 
# The decorator must preserve the original function’s name and docstring using functools.wraps.
# Apply it to a function compute_squares(n) that computes the sum of squares from 1 to n.

# Input:


# @timer

# def compute_squares(n):

# """Computes sum of squares from 1 to n."""

# return sum(i * i for i in range(1, n + 1))


# result = compute_squares(1_000_000)

# print(f"Result: {result}")

# print(f"Function name: {compute_squares.__name__}")

# print(f"Docstring: {compute_squares.__doc__}")


# Output:


# [timer] compute_squares executed in 0.0823s

# Result: 333333833333500000

# Function name: compute_squares

# Docstring: Computes sum of squares from 1 to n.


# Constraints:

# • Use functools.wraps to preserve function metadata

# • Time must be printed in seconds rounded to 4 decimal places

# • Format: [timer] <function_name> executed in <time>s

# • Decorator must work on any function with any number of argument

from functools import wraps
from datetime import datetime

def timer(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start=datetime.now()
        result=func(*args,**kwargs)
        print(result)
        print(f"The time taken is {datetime.now()-start}")
    return wrapper
        

@timer
def compute_squares(n):
    """Computes sum of squares from 1 to n."""
    return sum(i * i for i in range(1, n + 1))

compute_squares(100000)

#Question-2:

# Q2. @retry Decorator with Max Attempts

# Topics: Decorators with Arguments, Exception Handling, Closures

# Problem Statement:

# Write a parameterized decorator @retry(max_attempts) that retries a function up to max_attempts times
# if it raises an exception. After each failed attempt, print the attempt number and the error.
# If all attempts fail, raise the last exception. Apply it to a function fetch_data() 
# that simulates a flaky API call using random.choice.

# Input:

# import random

# random.seed(42) # For reproducible output

# @retry(max_attempts=5)

# def fetch_data():

# """Simulates a flaky API call."""

# if random.choice([True, False]):

# raise ConnectionError("Server unreachable")

# return {"status": "ok", "data": [1, 2, 3]}

# result = fetch_data()

# print(f"Result: {result}")

# Output:

# [retry] Attempt 1 failed: Server unreachable

# [retry] Attempt 2 succeeded!

# Result: {'status': 'ok', 'data': [1, 2, 3]}


# Constraints:

# • Decorator must accept max_attempts as a parameter

# • Print each failed attempt with attempt number and error message

# • Print success message with the attempt number that succeeded

# • If all attempts fail, raise the original exception with message: "All {max_attempts} attempts failed"

# • Use functools.wraps to preserve function metadata

from functools import wraps
import random

def retry(max_attempts):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            for i in range(max_attempts):
                try:
                    output=func()
                    print(f"[retry] Attempt {i+1} succeded")
                    print(output)
                    break
                except ConnectionError as e:
                    print(f"[retry] Attempt {i+1} and {e}")
        return wrapper
    return decorator
                



random.seed(42) # For reproducible output
@retry(max_attempts=5)
def fetch_data():
    """Simulates a flaky API call."""
    if random.choice([True, False]):
        raise ConnectionError("Server unreachable")
    return {"status": "ok", "data": [1, 2, 3]}


result = fetch_data()

print(f"Result: {result}")


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
    

# Q5. SQLAlchemy Models — Define User and Task with Relationships

# Topics: SQLAlchemy Models, Column Types, Foreign Key, relationship(), __repr__

# Problem Statement:

# Define two SQLAlchemy models matching your Day-2 schema:
# User (id, username, email, password, created_at) and Task (id, title, description, status, priority, owner_id as FK to users, created_at, updated_at).
# Set up a one-to-many relationship: a User has many Tasks. Add a __repr__ method to both models.

# Input:


# from models import User, Task


# user = User(username="alice", email="alice@mail.com", password="secure123")

# task = Task(title="Write report", status="pending", priority="high")

# print(repr(user))

# print(repr(task))


# Output:


# <User(id=None, username='alice', email='alice@mail.com')>

# <Task(id=None, title='Write report', status='pending', priority='high')>


# Constraints:

# • User: id (Integer, PK, auto-increment), username (String, unique, not null), email (String, unique), password (String, not null), created_at (DateTime, default=utcnow)

# • Task: id (Integer, PK, auto-increment), title (String, not null), description (Text, nullable), status (String, default="pending"), priority (String, default="medium"), owner_id (Integer, ForeignKey → users.id), created_at (DateTime, default=utcnow), updated_at (DateTime, default=utcnow, onupdate=utcnow)

# • Use relationship("Task", back_populates="owner") on User

# • Use relationship("User", back_populates="tasks") on Task

# • __repr__ must NOT include password

from datetime import datetime
from sqlalchemy import create_engine,Integer,String,Column,Text,DateTime,ForeignKey;
from sqlalchemy.orm import declarative_base,sessionmaker,relationship
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
print(DATABASE_URL)

engine=create_engine(DATABASE_URL,echo=False,future=True)

SessionLocal=sessionmaker(bing=engine,autoflush=False,autocommit=False)

Base=declarative_base()

class User(Base):
    
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,nullable=False,unique=False)
    email=Column(String,unique=True)
    password=Column(String,nullable=False)
    
    created_at=Column(DateTime,default=datetime.now())
    
    tasks=relationship("Task",back_populates='owner')
    
    def __repr__(self):
        return f" <User(id={self.id} email={self.email} name={self.username})"
    

class Task(Base):
    
    __tablename__="tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="pending")
    priority = Column(String, default="medium")
    
    created_at=Column(DateTime,default=datetime.now())
    updated_at=Column(DateTime,default=datetime.now(),onupdate=datetime.now())
    owner = relationship("User", back_populates="tasks")    
    def __repr__(self):
        return f"<Task(id:{self.id} title:{self.title} description:{self.description} status:{self.status})"
    

Base.metadata.create_all(bind=engine)
# print("Tables created successfully!")





# Q6. ORM CRUD — Create, Read, Update, Delete Operations

# Topics: session.add(), session.commit(), query, filter_by, delete

# Problem Statement:

# Using the models from Q5 and the session from Q4, write four functions: create_user(), get_all_users(), update_user_email(), and delete_user(). Each function must accept a session and relevant parameters, perform the operation, and return a confirmation message or the result.

# Input:


# from database import SessionLocal

# from crud import create_user, get_all_users, update_user_email, delete_user


# session = SessionLocal()


# # Create

# print(create_user(session, "charlie", "charlie@mail.com", "pass1234"))


# # Read

# users = get_all_users(session)

# for u in users:

# print(u)


# # Update

# print(update_user_email(session, "charlie", "charlie.new@mail.com"))


# # Delete

# print(delete_user(session, "charlie"))


# session.close()


# Output:


# User 'charlie' created with id 3

# <User(id=3, username='charlie', email='charlie@mail.com')>

# Updated charlie's email to charlie.new@mail.com

# User 'charlie' deleted successfully


# Constraints:

# • create_user(session, username, email, password) → adds user, commits, returns confirmation with generated id

# • get_all_users(session) → returns list of all User objects

# • update_user_email(session, username, new_email) → finds user by username, updates email, commits

# • delete_user(session, username) → finds user, deletes, commits

# • Raise ValueError with message "User '<username>' not found" if user doesn’t exist in update/delete

from sqlalchemy import create_engine,Column,Integer,String,DateTime,Text,Boolean,select
from sqlalchemy.orm import sessionmaker,declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

engine=create_engine(DATABASE_URL)

SessionLocal=sessionmaker(bind=engine)

Base=declarative_base()

class User(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)

Base.metadata.create_all(bind=engine)

def create_user(session,username:str,email:str,password:str):
    
    user=User(username=username,email=email,password=password)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    print(f"A new user ws created with the id {user.id}")

def get_users(session):
    stmt=select(User)
    results=session.execute(stmt)
    results=results.scalars().all()
    print(results)
    
    for result in results:
        print(result.id,result.username,result.email,result.password)

def update_users(sesssion,email:str,password:str):
    
    stmt=select(User).filter_by(email=email)
    
    user=session.execute(stmt).scalar_one_or_none()
    
    if user is None:
        pass
    else:
        user.password=password

    session.commit()    
    
def delete_user(sesssion,user_id:int):
    
    stmt=select(User).filter_by(id=user_id)
    
    user=session.execute(stmt).scalar()
    
    if user is None:
        raise ValueError(f"User with id {user_id} not found")
    else:
        session.delete(user)

    session.commit()  
    
    

session=SessionLocal()

# create_user(session,"Srinivasarao","srinivasarao@gmail.com","Aditya@369")
# create_user(session,"Rajyalakshmi","raji@gmail.com","Aditya@369")

get_users(session)
update_users(session,'aditya@gmail.com','UpdatedPassword')
print("\n\n")
get_users(session)

# delete_user(session,1)
print("\n\n")
get_users(session)

session.close()



# Q7. Querying — Filters, Sorting & Pagination

# Topics: filter(), filter_by(), order_by(), offset(), limit(), Relationships

# Problem Statement:

# Write three query functions using SQLAlchemy ORM: get_tasks_by_status() to filter tasks by status,
# get_tasks_sorted() to return tasks sorted by a given field, and get_tasks_paginated() 
# to return paginated results. Also write get_user_with_tasks() that fetches a user and accesses 
# their tasks via the relationship.

# Input:

# # Assume DB has: 5 tasks (3 pending, 2 completed) owned by alice and bob


# # Filter by status

# pending = get_tasks_by_status(session, "pending")

# print(f"Pending tasks: {len(pending)}")

# for t in pending:

# print(f" - {t.title} ({t.owner.username})")


# # Sorted

# sorted_tasks = get_tasks_sorted(session, sort_by="created_at", order="desc")

# print(f"\nSorted (newest first): {[t.title for t in sorted_tasks]}")


# # Paginated

# page = get_tasks_paginated(session, page=1, limit=2)

# print(f"\nPage 1 (limit 2): {[t.title for t in page]}")


# # User with tasks

# user = get_user_with_tasks(session, "alice")

# print(f"\n{user.username}'s tasks:")

# for t in user.tasks:

# print(f" - {t.title} ({t.status})")


# Output:


# Pending tasks: 3

# - Write report (alice)

# - Review PR (bob)

# - Fix bug (alice)


# Sorted (newest first): ['Fix bug', 'Deploy app', 'Review PR', 'Write report', 'Update docs']


# Page 1 (limit 2): ['Write report', 'Review PR']


# alice's tasks:

# - Write report (pending)

# - Fix bug (pending)

# - Deploy app (completed)


# Constraints:

# • get_tasks_by_status(session, status) → uses .filter_by(status=status)

# • get_tasks_sorted(session, sort_by, order) → uses .order_by() with desc() or asc()

# • get_tasks_paginated(session, page, limit) → uses .offset((page-1)*limit).limit(limit)

# • get_user_with_tasks(session, username) → accesses user.tasks via relationship

# • Return empty list (not error) if no results found

# • Default pagination: page=1, limit=1


from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,select,asc,desc
from sqlalchemy.orm import declarative_base, relationship,sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tasks")
    
def seed_data(session):
    alice = User(username="alice")
    bob = User(username="bob")

    session.add_all([alice, bob])
    session.commit()

    tasks = [
        Task(title="Write report", status="pending", owner=alice),
        Task(title="Fix bug", status="pending", owner=alice),
        Task(title="Deploy app", status="completed", owner=alice),
        Task(title="Review PR", status="pending", owner=bob),
        Task(title="Update docs", status="completed", owner=bob),
    ]

    session.add_all(tasks)
    session.commit()

Base.metadata.create_all(bind=engine)
SessionLocal=sessionmaker(bind=engine)
session=SessionLocal()
# seed_data(session)

stmt=select(Task)
results=session.execute(stmt).scalars().all()


def get_task_by_status(session,status):
    
    tasks=session.query(Task).filter_by(status=status).all()
    return tasks

def get_tasks_sorted(session,sort_by='created_at',order='asc'):
    
    column=getattr(Task,sort_by)
    
    if order=='asc':
        
        tasks=session.query(Task).order_by(asc(column)).all()
        print(tasks)
    else:
        tasks=session.query(Task).order_by(desc(column)).all()
    return tasks

def get_users(session,username):
    
    users=session.query(User).filter_by(username=username)
    return users

pending = get_task_by_status(session, "pending")

print(f"Pending tasks: {len(pending)}")
for t in pending:
    print(f" - {t.title} ({t.owner.username})")


sorted_tasks = get_tasks_sorted(session, sort_by="created_at", order="desc")

print(f"\nSorted (newest first): {[t.title for t in sorted_tasks]}")

user = get_users(session, "alice")



# Q8. Transactions — Atomic Operations with Rollback

# Topics: Transactions, ACID, commit(), rollback(), try/except

# Problem Statement:

# Write a function create_user_with_tasks() that creates a user and 3 default tasks in a single transaction. If any operation fails (e.g., duplicate username), the entire transaction must roll back — no partial data should be saved. Demonstrate both the success and failure cases.

# Input:


# # Case 1: Success

# print("--- Case 1: New user ---")

# result = create_user_with_tasks(session, "dave", "dave@mail.com", "pass1234",

# ["Setup environment", "Read documentation", "Complete onboarding"])

# print(result)


# # Case 2: Failure (duplicate username)

# print("\n--- Case 2: Duplicate user ---")

# result = create_user_with_tasks(session, "dave", "dave2@mail.com", "pass5678",

# ["Task A", "Task B", "Task C"])

# print(result)


# # Verify: dave should still have only 3 tasks (not 6)

# user = session.query(User).filter_by(username="dave").first()

# print(f"\ndave's total tasks: {len(user.tasks)}")


# Output:


# --- Case 1: New user ---

# Transaction successful: User 'dave' created with 3 tasks


# --- Case 2: Duplicate user ---

# Transaction rolled back: duplicate key value violates unique constraint

# dave2@mail.com was NOT saved


# dave's total tasks: 3


# Constraints:

# • Use try/except with session.rollback() on failure

# • Both user creation and all task inserts must be in the SAME transaction

# • On failure, print what was NOT saved to confirm rollback

# • Do NOT use session.begin_nested() — keep it simple with basic commit/rollback

# • Function signature: create_user_with_tasks(session, username, email, password, task_titles)
from sqlalchemy.exc import IntegrityError
def add_users_tasks(session,username,email,password,task_titles):
    
    try:
        user=User(username=username)
        session.add(user)
        session.flush()
        
        for title in task_titles:
            task=Task(title=title,status='pending',owner=user)
            session.add(task)
        session.commit()
        return f"Transection successful"
    except IntegrityError as e:
        session.rollback()
        return f"Trancsaction rolled back with email {email}"

result = add_users_tasks(
    session,
    "dave",
    "dave@mail.com",
    "pass1234",
    ["Setup environment", "Read documentation", "Complete onboarding"]
)
print(result)



from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker



engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True
)

Session = sessionmaker(bind=engine)


# Q9. Connection Pooling — Configure & Monitor

# Topics: Connection Pooling, pool_size, max_overflow, pool_pre_ping

# Problem Statement:

# Configure SQLAlchemy’s connection pool for your Supabase connection with specific settings. Write a script that creates the engine with pool configuration, opens multiple sessions, prints the pool status after each, and properly closes all sessions.

# Input:


# from sqlalchemy import create_engine, text


# engine = create_engine(

# DATABASE_URL,

# pool_size=5,

# max_overflow=10,

# pool_timeout=30,

# pool_recycle=1800,

# pool_pre_ping=True

# )


# Session = sessionmaker(bind=engine)


# # Open 3 sessions and check pool

# sessions = []

# for i in range(3):

# s = Session()

# s.execute(text("SELECT 1")) # Force connection checkout

# sessions.append(s)

# print(f"After opening session {i+1}: {engine.pool.status()}")


# # Close all sessions

# for s in sessions:

# s.close()

# print(f"\nAfter closing all: {engine.pool.status()}")


# Output:



# # After opening session 1: Pool size: 5 Connections in pool: 0 Current Overflow: 0 Current Checked out connections: 1

# # After opening session 2: Pool size: 5 Connections in pool: 0 Current Overflow: 0 Current Checked out connections: 2

# # After opening session 3: Pool size: 5 Connections in pool: 0 Current Overflow: 0 Current Checked out connections: 3


# # After closing all: Pool size: 5 Connections in pool: 3 Current Overflow: 0 Current Checked out connections: 0


# # Constraints:

# # • Set pool_size=5, max_overflow=10, pool_timeout=30, pool_recycle=1800

# # • Set pool_pre_ping=True (required for Supabase to handle dropped connections)

# # • Print pool status using engine.pool.status() after each session open and after all close

# # • Explain in a comment why each pool setting matters

# # • All sessions must be properly closed at the end

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")



SessionLocal=sessionmaker(bind=engine)

sessions = []
for i in range(3):
    s = SessionLocal()
    s.execute(text("SELECT 1"))
    sessions.append(s)
print(f"After opening session {i+1}: {engine.pool.status()}")

for s in sessions:
    s.close()

print(f"After closing all sessions {engine.pool.status()}")


# Q10. Alembic — Initialize, Migrate & Rollback

# Topics: Alembic, Database Migration, Autogenerate, Upgrade, Downgrade

# Problem Statement:

# Set up Alembic in your project to manage database migrations against your Supabase database. Perform three operations: (a) Initialize Alembic and configure it to use your DATABASE_URL from .env, (b) Generate an autogenerated migration from your User and Task models, (c) Add a new due_date column to the Task model, generate a second migration, apply it, then rollback it.

# Input (Step-by-step commands):


# # Step 1: Initialize Alembic

# alembic init alembic


# # Step 2: Configure alembic/env.py to use your models and DATABASE_URL

# # (modify env.py — see constraints below)


# # Step 3: Generate first migration

# alembic revision --autogenerate -m "create users and tasks tables"

# # Step 4: Apply migration

# alembic upgrade head


# # Step 5: Verify

# alembic current


# # Step 6: Add due_date to Task model, then:

# alembic revision --autogenerate -m "add due_date to tasks"

# alembic upgrade head


# # Step 7: Rollback the due_date migration

# alembic downgrade -1


# # Step 8: Verify rollback

# alembic current


# Output:


# # Step 3

# INFO [alembic.autogenerate.compare] Detected added table 'users'

# INFO [alembic.autogenerate.compare] Detected added table 'tasks'

# Generating alembic/versions/abc123_create_users_and_tasks_tables.py ... done


# # Step 4

# INFO [alembic.runtime.migration] Running upgrade -> abc123, create users and tasks tables


# # Step 5

# abc123 (head)


# # Step 6

# INFO [alembic.autogenerate.compare] Detected added column 'tasks.due_date'

# INFO [alembic.runtime.migration] Running upgrade abc123 -> def456, add due_date to tasks


# # Step 7

# INFO [alembic.runtime.migration] Running downgrade def456 -> abc123, add due_date to tasks

# # Step 8
# abc123

# Constraints:

# • In alembic/env.py: import your Base from models and set target_metadata = Base.metadata

# • In alembic.ini: set sqlalchemy.url to your Supabase DATABASE_URL (or load from .env in env.py)

# • due_date column: Column(DateTime, nullable=True)

# • After rollback, verify the due_date column no longer exists by querying information_schema.columns

# • Commit all migration files to version control (do NOT add them to .gitignore)

# • Each migration file must have both upgrade() and downgrade() functions

