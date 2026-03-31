from fastapi import APIRouter,BackgroundTasks
from services.task_service import create_task
from schemas.schema import TaskInput,TaskResponse
from services.task_service import get_tasks,get_task_id,get_task_status
from typing import List
from datetime import datetime

router=APIRouter()

@router.get("/")
def routerhome():
    result=get_tasks()
    return result

def log_msg(url):
    with open("post_log.txt",'a') as file:
        file.write(f"\n{datetime.now()}  Method: POST To URL {url}\n")
        
        
@router.post("/")
def addtask(task:TaskInput,background_tasks:BackgroundTasks):
    
    taskdict=task.model_dump()
    print(taskdict)
    # try:
    #     create_task(taskdict.id,taskdict.name,taskdict.status)
    #     return {"message":"Task was added"}
    # except:
    #     return {"message":"Problem in creating task"}
    result=create_task(taskdict['id'],taskdict['name'],taskdict['status'])
    background_tasks.add_task(log_msg,"/tasks")
    return {"message":result}

@router.get("/id/{task_id}")
def get_task_by_id(task_id:int):
    result=get_task_id(task_id)
    return result

@router.get("/status/{task_status}")
def get_task_by_status(task_status:str):
    result=get_task_status(task_status)
    return result

