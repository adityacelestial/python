from fastapi import APIRouter
from schemas.pyschemas import UserCreate,UserResponse,UserLogin
from services.user_service import UserService
from database.models import session
route=APIRouter()

@route.get("/")
def userhome():
    return "This is home user"

@route.post("/register", response_model=UserResponse, status_code=201)
def registeruser(user:UserCreate):
    userdict=user.model_dump()
    
    userserve=UserService(session)
    result=userserve.create_user(userdict)
    
    return result
    
@route.post("/login")
def loginuser(cred:UserLogin):
    creddict=cred.model_dump()
    userserve=UserService(session)
    result=userserve.login_user(creddict)
    return result
    
