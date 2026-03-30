from fastapi import FastAPI, Depends, HTTPException
from routes import auth_routes,loan_routes,admin_routes
from services.analytics import analysis
from security import get_current_user
app=FastAPI()

app.include_router(router=auth_routes.route,prefix="/auth")
app.include_router(router=loan_routes.route,prefix="/loan")
app.include_router(router=admin_routes.route,prefix="/admin")
@app.get("/")
def homepage():
    return {"message":"This is a Home page"}

@app.get("/health",status_code=200)
def health_res():
    return {"message":"The Backend is up and running succesfully"}

@app.get("/analytics/summary/{user_id}", dependencies=[Depends(get_current_user)])
def summary(user_id: int, current_user: dict = Depends(get_current_user)):
    if user_id != current_user.get("user_id"):
        raise HTTPException(status_code=403, detail="Access denied")
    result=analysis(user_id)
    return result
    