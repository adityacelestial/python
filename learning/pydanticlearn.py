from pydantic import BaseModel

class User(BaseModel):
    name:str
    age:int

user=User(name="Aditya",age=22)
print(user)
user=User(name="Aditya",age="24")
print(user)

# pydantic throws error when there is no integer

# user=User(name="Aditya",age="abx")
# print(user)

# deffault values

class Major(BaseModel):
    name:str
    age:int =18

major=Major(name="Aditya")
print(major)
major=Major(name="Ad",age=10)
print(major)

#optional fields
