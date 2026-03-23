from fastapi import APIRouter, Depends
from repositories.json_repository import JSONRepository
from services.task_service import TaskService
from models.schemas import TaskCreate, TaskUpdate
from config import DATA_PATH

router = APIRouter()

def get_service():
    repo = JSONRepository(f"{DATA_PATH}/tasks.json", "tasks")
    return TaskService(repo)

@router.post("/")
def create(task: TaskCreate, service: TaskService = Depends(get_service)):
    return service.create(task, owner="alice")

@router.get("/")
def get_tasks(status: str = None, priority: str = None, service: TaskService = Depends(get_service)):
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