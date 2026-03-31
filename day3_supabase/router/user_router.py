from fastapi import APIRouter, BackgroundTasks, Header, HTTPException
from typing import Optional
from schemas.schema import UserInput, AuthInput
from services.user_service import create_user, get_user_id, get_users
from services.supabase_service import sign_up, sign_in, get_user
from datetime import datetime

router = APIRouter()


@router.get("/")
def getusers():
    result = get_users()
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


@router.post("/signup")
def supabase_signup(payload: AuthInput):
    result = sign_up(payload.email, payload.password)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=str(result["error"]))
    return {"message": "User signup triggered", "data": result}


@router.post("/signin")
def supabase_signin(payload: AuthInput):
    result = sign_in(payload.email, payload.password)
    if result.get("error"):
        raise HTTPException(status_code=401, detail=str(result["error"]))
    return {"message": "User signed in", "data": result}


@router.get("/me")
def supabase_me(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.split("Bearer ")[1]
    result = get_user(token)
    if result.get("error"):
        raise HTTPException(status_code=401, detail=str(result["error"]))
    return {"message": "User info", "data": result}