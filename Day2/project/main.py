from fastapi import FastAPI
from routers import user_router, task_router
from middleware.logging_middleware import LoggingMiddleware

app = FastAPI()

app.add_middleware(LoggingMiddleware)

app.include_router(user_router.router, prefix="/users")
app.include_router(task_router.router, prefix="/tasks")

@app.get("/")
def root():
    return {"message": "Task API Running"}