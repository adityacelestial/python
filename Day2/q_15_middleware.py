from fastapi import FastAPI,Request
from datetime import datetime

app=FastAPI()

@app.middleware('http')

async def handle_middleware(request:Request,call_next):
    logtime=datetime.now().strftime("%Y-%M-%D %H:%M:%S")
    
    response=await call_next(request)
    logstring=f"{logtime} Request: {request.method} URL:{request.url} Responsecode:{response.status_code}"
    with open("requestlog.txt",'a') as file:
        file.write(logstring+"\n")
    return response


@app.get("\tasks")
def handle_get():
    pass

@app.put("\tasks")
def handle_get():
    pass
@app.post("\tasks")
def handle_get():
    pass
@app.delete("\tasks")
def handle_get():
    pass
    