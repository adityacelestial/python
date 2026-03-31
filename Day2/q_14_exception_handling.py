# Q14. Custom Exception Handler in FastAPI 

# Topics: FastAPI, Error Handling 

# Problem Statement: 

# Add a custom exception class TaskNotFoundError and register a global exception handler in FastAPI that returns a structured JSON error response with proper status code. 

# Input: 

# # GET /tasks/999 (non-existent) 

# Output: 

# # Response (404) 

# {"error": "TaskNotFoundError", "message": "Task with id 999 not found", "status_code": 404} 

# Constraints: 

# Create a custom exception class inheriting from Exception 

# Use @app.exception_handler() decorator 

# Response must always have error, message, and status_code fields 

# Apply this handler to all relevant endpoints 



from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
import json
app=FastAPI()

def read_data():
    with open("tasks.json",'r') as file:
        data=json.load(file)
    return data

class TaskNotFoundException(Exception):
    def __init__(self,task_id):
        self.task_id=task_id
        self.message=f"The task with {task_id} was not found"
        
@app.exception_handler(TaskNotFoundException)
def handle_not_found(request:Request,exe:TaskNotFoundException):
    
    return JSONResponse(
        status_code=404,
        content={
            "message":exe.message
        }
    )

@app.get("/tasks/{task_id}")
def handle_get(task_id:int):
    data=read_data()
    for i in data:
        if(i['task_id']==task_id):
            return i
    raise TaskNotFoundException(task_id)
