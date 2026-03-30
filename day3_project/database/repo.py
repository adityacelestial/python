
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
SessionLocal=sessionmaker()

engine=create_engine(url=DATABASE_URL)
session=SessionLocal(bind=engine)

# from models import User

# user=User(id=1,name="Aditya")

# session.add(user)
# session.commit()


