from fastapi import FastAPI
from router import task_router
from router import user_router
from datetime import datetime
from fastapi import Request
app=FastAPI()


app.include_router(router=task_router.router,prefix="/task")
app.include_router(router=user_router.router,prefix="/user")

 

@app.get("/")
def home():
    return {"message":"This is a Home page"}
