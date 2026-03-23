# Q13. FastAPI — Health Check and CRUD Endpoints 

# Topics: FastAPI, Pydantic, REST, HTTP Methods 

# Problem Statement: 

# Create a FastAPI application with the following endpoints for a Task resource (store tasks in a Python list in memory): 

# GET /health — returns {"status": "healthy"} 

# POST /tasks — create a new task 

# GET /tasks — list all tasks with optional ?status= filter 

# GET /tasks/{task_id} — get task by ID 

# PUT /tasks/{task_id} — update a task 

# DELETE /tasks/{task_id} — delete a task 

# Input: 

# # POST /tasks 

# {"title": "Write report", "description": "Q2 summary", "status": "pending"} 

 

# # GET /tasks?status=pending 

# Output: 

# # POST response (201) 

# {"id": 1, "title": "Write report", "description": "Q2 summary", "status": "pending"} 

 

# # GET response (200) 

# [{"id": 1, "title": "Write report", ...}] 

# Constraints: 

# Use Pydantic models: TaskCreate, TaskUpdate, TaskResponse 

# Task ID must be auto-generated (incrementing integer) 

# Status must be one of: pending, in_progress, completed 

# Return 404 if task not found 

# Return 201 on successful creation 

# Test all endpoints via Postman 

from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

app = FastAPI()

# In-memory storage
tasks = []
task_id_counter = 1

# ✅ Allowed status values
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


# 🩺 Health Check
@app.get("/health")
def health():
    return {"status": "healthy"}


# ➕ Create Task
@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    global task_id_counter

    new_task = {
        "id": task_id_counter,
        **task.model_dump()
    }

    tasks.append(new_task)
    task_id_counter += 1

    return new_task


# 📄 Get All Tasks (with optional filter)
@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(status: Optional[TaskStatus] = Query(None)):
    if status:
        return [task for task in tasks if task["status"] == status]
    return tasks


# 🔍 Get Task by ID
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


# ✏️ Update Task
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            update_data = updated.model_dump(exclude_unset=True)
            task.update(update_data)
            return task
    raise HTTPException(status_code=404, detail="Task not found")


# ❌ Delete Task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")