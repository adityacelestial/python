from fastapi import APIRouter
from fastapi import BackgroundTasks
from schemas.schema import UserInput
from services.user_service import create_user,get_user_id,get_users
from datetime import datetime
router=APIRouter()

@router.get("/")
def getusers():
    result=get_users()
    return result


def log_msg(url):
    with open("post_log.txt",'a') as file:
        file.write(f"\n{datetime.now()}  Method: POST To URL {url}\n")
        

@router.post("/")
def insert_into_user(user:UserInput,background_taks:BackgroundTasks):
    userdict=user.model_dump()
    result=create_user(userdict["id"],userdict["name"])
    background_taks.add_task(log_msg,"/users")
    return result


@router.get("/id/{user_id}")
def get_user_by_id(user_id:int):
    
    result=get_user_id(user_id)
    return result