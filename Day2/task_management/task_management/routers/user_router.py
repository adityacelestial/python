import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from models.schemas import UserCreate, UserLogin, UserResponse
from repositories.json_repository import JSONRepository
from services.user_service import UserService
from config import settings

router = APIRouter(prefix="/users", tags=["Users"])
logger = logging.getLogger(__name__)


# ──────────────── Dependency injection ────────────────

def get_user_service() -> UserService:
    repo = JSONRepository(settings.users_file, "users")
    return UserService(repo)


# ──────────────── Endpoints ────────────────

@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
):
    user = service.register(payload.username, payload.email, payload.password)
    return user


@router.post("/login", status_code=200)
def login_user(
    payload: UserLogin,
    service: UserService = Depends(get_user_service),
):
    user = service.login(payload.username, payload.password)
    return {"message": "Login successful", "username": user["username"]}


@router.get("", response_model=List[UserResponse])
def list_users(service: UserService = Depends(get_user_service)):
    return service.list_users()


@router.delete("/{user_id}", status_code=200)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    service.delete_user(user_id)
    return {"message": f"User {user_id} deleted successfully"}
