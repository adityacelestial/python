# Q15. Request Logging Middleware 

# Topics: FastAPI, Middleware, Logging 

# Problem Statement: 

# Add a middleware to the FastAPI app that logs every incoming request with: timestamp, HTTP method, path, and response status code. Write logs to api_logs.txt. 

# Input: 

# # Any request: GET /tasks 

# Output: 

# # Log entry in api_logs.txt: 

# 2026-03-20 14:30:00 | GET /tasks | Status: 200 | Time: 12ms 

# Constraints: 

# Use @app.middleware("http") 

# Calculate response time in milliseconds 

# Log to file, not just console 

# Include timestamp, method, path, status code, and duration 


from fastapi import FastAPI, Request
import time
from datetime import datetime

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = int((time.time() - start_time) * 1000)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_line = (
        f"{timestamp} | {request.method} {request.url.path} "
        f"| Status: {response.status_code} | Time: {duration}ms\n"
    )

    with open("api_logs.txt", "a") as file:
        file.write(log_line)

    return response
