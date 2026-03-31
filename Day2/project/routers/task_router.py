from fastapi import APIRouter, Depends, BackgroundTasks
from datetime import datetime

from repositories.json_repository import JSONRepository
from services.task_service import TaskService
from models.schemas import TaskCreate, TaskUpdate

router = APIRouter()



def log_notification(title: str, owner: str):
    with open("notifications.log", "a") as f:
        f.write(f"[{datetime.utcnow().isoformat()}] "
                f"Task '{title}' created by {owner} — notification sent\n")


from config import DATA_PATH


def get_service():
    repo = JSONRepository(f"{DATA_PATH}/tasks.json", "tasks")
    return TaskService(repo)


@router.post("/")
def create_task(
    task: TaskCreate,
    background_tasks: BackgroundTasks,
    service: TaskService = Depends(get_service)
):
    new_task = service.create(task, owner="alice")

    # background process
    background_tasks.add_task(log_notification, task.title, "alice")

    return new_task


@router.get("/")
def get_tasks(
    status: str = None,
    priority: str = None,
    service: TaskService = Depends(get_service)
):
    filters = {"status": status, "priority": priority}
    return service.get_all(filters)


@router.get("/{task_id}")
def get_task(task_id: int, service: TaskService = Depends(get_service)):
    return service.get_by_id(task_id)


@router.put("/{task_id}")
def update_task(
    task_id: int,
    data: TaskUpdate,
    service: TaskService = Depends(get_service)
):
    return service.update(task_id, data.dict(exclude_unset=True))


@router.delete("/{task_id}")
def delete_task(task_id: int, service: TaskService = Depends(get_service)):
    service.delete(task_id)
    return {"message": "Deleted"}