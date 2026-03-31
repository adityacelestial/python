
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


