from fastapi import FastAPI
from routers import task_router
from middleware.logging_middleware import LoggingMiddleware

app = FastAPI()

app.add_middleware(LoggingMiddleware)
app.include_router(task_router.router)

@app.get("/")
def root():
    return {"message": "Task API running"}