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



