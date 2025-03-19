from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import db
import database as db

app = FastAPI()

SECRET_KEY = "Ore wa monkey d luffy !!Kaizoku-o ni ore wa naru"

class User(BaseModel):
    name: str
    email: str
    password: str
    aadhar: str
    phone_number: str
    location: str
    is_officer: bool

@app.get("/")
def index():
    return {"message": "hello everyone"}

item = {
    "hello": "hi"
}

@app.get("/getitem/{item_string}")
def get(item_string: str):
    if item_string in item:
        return item[item_string]
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/user/signup")
def signup(user: User):
    if db.get_user(user.name):
        raise HTTPException(status_code=400, detail="User already exists")
    
    db.add_user(user)
    return {"message": "User registered successfully"}

@app.get("/user/{name}")
def get_user(name: str):
    user = db.get_user(name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
