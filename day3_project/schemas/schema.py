from pydantic import BaseModel

class TaskInput(BaseModel):
    id:int
    name:str
    status:str
    
class TaskResponse(BaseModel):
    task_id:int
    task_name:str
    task_status:str
    
    
    class Config:
            orm_mode = True

class UserInput(BaseModel):
    id:int
    name:str



