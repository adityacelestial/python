from fastapi import FastAPI


app=FastAPI()

@app.get("/")
def home():
    return {"Message":"This is homepage"}

@app.get("/users")
def getusers():
    return ["Aditya",'srinivasarao']

#path parameters
@app.get("/users/{user_id}")
def get_user(user_id):
    return f"WE got reqiest for user {user_id}"

# query parameters

@app.get("/search")
def search(q,q1):
    return {"query":q,"query1":q1}



