from fastapi import FastAPI
from database import db
from models import User
app = FastAPI()


SECRET_KEY="Ore wa monkey d luffy !!Kaizoku-o ni ore wa naru"


# tested the working 
@app.get("/")
def index():
    return {"message": "hello everyone"}

item={
    "hello":"hi"
}
@app.get("/getitem/{item_string}")
def get(item_string:str):
    return item[item_string]

#user authentication
@app.post("/user/register")
def signup(User:User):
    db.add_user(User)
    return {"message":"user registered successfully"}

@app.get("/user/{name}")
def get_user(name:str):
    return db.get_user(name)

