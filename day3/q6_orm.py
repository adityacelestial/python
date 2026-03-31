
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



