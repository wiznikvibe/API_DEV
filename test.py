from fastapi import FastAPI
from fastapi.params import Body


app = FastAPI()

@app.get("/")
def root():
    return {"message":"Hello WOrld !"}

@app.get("/posts")
def get_post():
    return {"data": "This is your posts."}

@app.post("/createposts")
def create_posts(payLoad: dict= Body(...)):
    return {"message": "successfully created posts"}
