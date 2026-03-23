from fastapi import APIRouter, Depends
from repositories.json_repository import JSONRepository
from services.user_service import UserService
from models.schemas import UserCreate, UserLogin
from config import DATA_PATH

router = APIRouter()

def get_service():
    repo = JSONRepository(f"{DATA_PATH}/users.json", "users")
    return UserService(repo)

@router.post("/register")
def register(user: UserCreate, service: UserService = Depends(get_service)):
    return service.register(user)

@router.post("/login")
def login(user: UserLogin, service: UserService = Depends(get_service)):
    return service.login(user)

@router.get("/")
def get_users(service: UserService = Depends(get_service)):
    return service.get_all()

@router.delete("/{user_id}")
def delete_user(user_id: int, service: UserService = Depends(get_service)):
    service.delete(user_id)
    return {"message": "Deleted"}