from fastapi import FastAPI,status,Query,HTTPException
from pydantic import BaseModel
import json
from typing import Optional,Literal,List

TaskStatus=Literal['pending','on-prigress','completed']

app=FastAPI()
serial=0
@app.get("/health")
def healthpage():
    return {"message":"Health OK"}


def read_json(path):
    with open(path,'r') as file:
        data=json.load(file)
    return data

def write_json(path,data):
    with open(path,'w') as file:
        json.dump(data,file,indent=4)
    

class TaskCreate(BaseModel):
    taskname:str
    task_status:str

class TaskUpdate(BaseModel):
    taskid:Optional[int]=None
    taskname:Optional[str]=None
    task_status:Optional[str]=None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus

@app.post("/task",response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task:TaskCreate):
    sampledict=task.model_dump()
    global serial
    
    sampledict["task_id"]=serial+1
    serial=serial+1
    data=read_json("tasks.json")
    data.append(sampledict)
    write_json("tasks.json",data)

@app.get("/task")
def get_tasks(status):
    data=read_json("tasks.json")
    if(status!=''):
        data=list(filter(lambda x:x['task_status']==status,data))
        return data
    else:
        return data
    

@app.get("/tasks/{task_id}")
def get_task_task_id(task_id:int):
    data=read_json("tasks.json")
    output= list(filter(lambda x:x['task_id']==task_id,data))
    print(output)
    return output

@app.put("/tasks/{task_id}")
def update_task_task_id(task_id,updated:TaskUpdate):
    sampledict=updated.model_dump()
    data=read_json("tasks.json")
    for task in data:
        if task['task_id']==task_id:
            task.update(sampledict)
        with open("tasks.json",'w') as file:
            file.write(data)
        return
    raise HTTPException(status_code=404, detail="Task not found")
    

@app.delete("/tasks/{task_id}")
def delete_task(task_id):
    data=read_json("tasks.json")
    final_data=list(filter(lambda x:x['task_id']!=task_id,data))
    if(len(final_data)==0):
        raise HTTPException(status_code=404, detail="Task not found")
    with open("tasks.json",'w') as file:
        json.dump(final_data,file,indent=4)
        return





    
    
    