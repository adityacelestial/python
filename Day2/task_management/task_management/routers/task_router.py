import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from models.enums import TaskPriority, TaskStatus
from models.schemas import TaskCreate, TaskResponse, TaskUpdate
from repositories.json_repository import JSONRepository
from services.task_service import TaskService
from config import settings

router = APIRouter(prefix="/tasks", tags=["Tasks"])
logger = logging.getLogger(__name__)


# ──────────────── Dependency injection ────────────────

def get_task_service() -> TaskService:
    repo = JSONRepository(settings.tasks_file, "tasks")
    return TaskService(repo)


# ──────────────── Endpoints ────────────────

@router.post("", response_model=TaskResponse, status_code=201)
def create_task(
    payload: TaskCreate,
    service: TaskService = Depends(get_task_service),
):
    return service.create_task(
        title=payload.title,
        owner=payload.owner,
        priority=payload.priority,
        status=payload.status,
        description=payload.description,
    )


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    status: Optional[TaskStatus] = Query(default=None),
    priority: Optional[TaskPriority] = Query(default=None),
    owner: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    service: TaskService = Depends(get_task_service),
):
    return service.list_tasks(
        status=status,
        priority=priority,
        owner=owner,
        page=page,
        limit=limit,
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    return service.get_task(task_id)


@router.put("/{task_id}", response_model=TaskResponse)
def full_update_task(
    task_id: int,
    payload: TaskCreate,
    service: TaskService = Depends(get_task_service),
):
    updates = {
        "title": payload.title,
        "description": payload.description,
        "priority": payload.priority,
        "status": payload.status,
        "owner": payload.owner,
    }
    return service.update_task(task_id, updates)


@router.patch("/{task_id}", response_model=TaskResponse)
def partial_update_task(
    task_id: int,
    payload: TaskUpdate,
    service: TaskService = Depends(get_task_service),
):
    updates = payload.model_dump(exclude_none=True)
    return service.update_task(task_id, updates)


@router.delete("/{task_id}", status_code=200)
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    service.delete_task(task_id)
    return {"message": f"Task {task_id} deleted successfully"}
