from fastapi import APIRouter, Depends
from services.task_service import TaskService
from repositories.json_repository import JSONRepository
from config import settings

router = APIRouter(prefix="/tasks")

def get_task_service():
    repo = JSONRepository(settings.TASK_FILE, "tasks")
    return TaskService(repo)

@router.post("/")
def create_task(task, service: TaskService = Depends(get_task_service)):
    return service.create_task(task, owner="alice")