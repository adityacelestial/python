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
