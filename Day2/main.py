from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# In-memory "database"
tasks = []
task_id_counter = 1

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str = Field(..., pattern="^(pending|completed)$")


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = Field(..., pattern="^(pending|completed)$")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    global task_id_counter
    new_task = Task(id=task_id_counter, **task.dict())
    tasks.append(new_task)
    task_id_counter += 1
    return new_task


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, update: TaskCreate):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = Task(id=task_id, **update.dict())
            tasks[i] = updated_task
            return updated_task

    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail="Task not found")