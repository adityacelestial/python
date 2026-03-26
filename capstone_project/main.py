from fastapi import FastAPI
from routes import auth_routes,loan_routes,admin_routes
from services.analytics import analysis
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

@app.get("/analytics/summary/{user_id}")
def summary(user_id):
    
    result=analysis(user_id)
    return result
    