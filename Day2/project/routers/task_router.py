from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from repositories.sqlalchemy_repository import SQLAlchemyRepository
from services.task_service import TaskService
from models.schemas import TaskCreate, TaskUpdate
from database import get_db
from datetime import datetime

router = APIRouter()


# ✅ Background task function
def log_notification(title: str, owner: str):
    with open("notifications.log", "a") as f:
        f.write(f"[{datetime.utcnow()}] Task '{title}' created by {owner} — notification sent\n")


# ✅ Dependency injection (DB instead of JSON file)
def get_service(db: Session = Depends(get_db)):
    repo = SQLAlchemyRepository(db)
    return TaskService(repo)


@router.post("/")
def create(
    task: TaskCreate,
    background_tasks: BackgroundTasks,
    service: TaskService = Depends(get_service)
):
    new_task = service.create(task, owner="alice")

    # ✅ Background logging
    background_tasks.add_task(
        log_notification,
        task.title,
        "alice"
    )

    return new_task


@router.get("/")
def get_tasks(
    status: str = None,
    priority: str = None,
    service: TaskService = Depends(get_service)
):
    return service.get_all({"status": status, "priority": priority})


@router.get("/{task_id}")
def get_task(task_id: int, service: TaskService = Depends(get_service)):
    return service.get_by_id(task_id)


@router.put("/{task_id}")
def update(task_id: int, data: TaskUpdate, service: TaskService = Depends(get_service)):
    return service.update(task_id, data.dict(exclude_unset=True))


@router.delete("/{task_id}")
def delete(task_id: int, service: TaskService = Depends(get_service)):
    service.delete(task_id)
    return {"message": "Deleted"}