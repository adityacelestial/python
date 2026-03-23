from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Literal

app = FastAPI()

# In-memory DB
tasks = []
task_id_counter = 1

TaskStatus = Literal["pending", "in_progress", "completed"]


# 📦 Models
class TaskCreate(BaseModel):
    title: str
    description: str
    status: TaskStatus


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus


# ✅ Custom Exception
class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id
        self.message = f"Task with id {task_id} not found"


# ✅ Global Exception Handler
@app.exception_handler(TaskNotFoundError)
def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "TaskNotFoundError",
            "message": exc.message,
            "status_code": 404
        }
    )


# ➕ Create Task
@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    global task_id_counter

    new_task = {
        "id": task_id_counter,
        **task.model_dump()
    }

    tasks.append(new_task)
    task_id_counter += 1
    return new_task


# 📄 Get All Tasks
@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    return tasks


# 🔍 Get Task by ID
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise TaskNotFoundError(task_id)


# ✏️ Update Task
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            task.update(updated.model_dump(exclude_unset=True))
            return task
    raise TaskNotFoundError(task_id)


# ❌ Delete Task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return {"message": "Task deleted"}
    raise TaskNotFoundError(task_id)