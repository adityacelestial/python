from sqlalchemy import create_engine,Integer,String,DateTime,Float,Column
from sqlalchemy.orm import sessionmaker,declarative_base,relationship
from datetime import datetime
Base=declarative_base()


class User(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True)
    name=Column(String)
    age=Column(Integer)
    
    
class Task(Base):
    __tablename__="task"
    
    task_id=Column(Integer,primary_key=True,index=True)
    task_name=Column(String,nullable=False)
    task_status=Column(String)
    created_at=Column(DateTime,default=datetime.now())
    
    
    
    

    

    
