from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import db
import database as db
import hashlib
import hmac

from models import Query

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

def encode_password(password: str) -> str:
        return hmac.new(SECRET_KEY.encode(), password.encode(), hashlib.sha256).hexdigest()

    
@app.post("/user/login")
def login(email: str, password: str):
    encoded_password = encode_password(password)
    user = db.get_user_by_email(email)
    if not user or user.password != encoded_password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful"}
@app.get("/news/{location}")
def get_news_by_location(location: str):
    news = db.get_news_by_location(location)
    if not news:
        raise HTTPException(status_code=404, detail="No news found for the given location")
    return news


@app.post("/user/query")
def post_query(query: Query):
    user = db.get_user(query.user_name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.add_query(query)
    return {"message": "Query posted successfully"}

@app.post("/news")
def post_news(news: dict, user_name: str):
    user = db.get_user(user_name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_officer:
        raise HTTPException(status_code=403, detail="Only officers can post news")
    db.add_news(news)
    return {"message": "News posted successfully"}


@app.get("/queries")
def get_queries(location: str, department: str):
    queries = db.get_queries_by_location_and_department(location, department)
    if not queries:
        raise HTTPException(status_code=404, detail="No queries found for the given location and department")
    return queries

@app.post("/queries/answer")
def post_answer(query_id: int, answer: str, user_name: str):
    user = db.get_user(user_name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_officer:
        raise HTTPException(status_code=403, detail="Only officers can post answers")
        
    query = db.get_query_by_id(query_id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    if query.department != user.department:
        raise HTTPException(status_code=403, detail="You can only answer queries from your department")
        
    db.add_answer_to_query(query_id, answer, user_name)
    return {"message": "Answer posted successfully"}

