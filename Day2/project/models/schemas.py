from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from .enums import TaskStatus, TaskPriority

# -------- USER --------
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

# -------- TASK --------
class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    priority: TaskPriority
    status: TaskStatus = TaskStatus.pending

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    priority: Optional[TaskPriority]
    status: Optional[TaskStatus]

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    owner: str
    created_at: datetime
    updated_at: datetime