from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import db
import database as db
import hashlib
import hmac
from models import News
from models import LoginData
from models import Query
from models import Answer
from mangum import Mangum
from database import SECRET_KEY
app = FastAPI()
handler = Mangum(app)

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
    if db.get_user(user.email):
        raise HTTPException(status_code=400, detail="User already exists")
    db.add_user(user)
    return {"message": "User registered successfully"}

@app.get("/user/{email}")
def get_user(email:str):
    user = db.get_user(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def encode_password(password: str) -> str:
    return hmac.new(SECRET_KEY.encode(), password.encode(), hashlib.sha256).hexdigest()
    
@app.post("/user/login")
def login(data: LoginData):
    if not db.get_user(data.email):
        raise HTTPException(status_code=404, detail="User not found")
    if db.get_user(data.email)["password"] != encode_password(data.password):
        print(encode_password(data.password))
        raise HTTPException(status_code=401, detail="Invalid password")
    return {"message": "Login successful"}

@app.get("/news/{location}")
def get_news_by_location(location: str):
    news = db.get_news_by_location(location)
    if not news:
        raise HTTPException(status_code=404, detail="No news found for the given location")
    return news


@app.post("/add-query")
def post_query(query: Query):
    user = db.get_user(query.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.add_query(query)
    return {"message": "Query posted successfully"}

@app.post("/add-news")
def post_news(news: News):
    user = db.get_user(news.email)  # Fetch user by email
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user["is_officer"]:  # Fix: Accessing the attribute correctly
        raise HTTPException(status_code=403, detail="Only officers can post news")
    
    db.add_news(news.dict())  # Store news in DB
    return {"message": "News posted successfully"}

@app.get("/queries/{location}/{department}")
def get_queries(location, department):
    queries = db.get_queries_by_location_and_department(location, department)
    if not queries:
        raise HTTPException(status_code=404, detail="No queries found for the given location and department")
    return queries

@app.post("/queries/answer")
def post_answer(answer:Answer):
    user = db.get_user(answer.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user['is_officer']:
        raise HTTPException(status_code=403, detail="Only officers can post answers")
        
    query = db.get_query_by_id(answer.query_id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    db.add_answer_to_query(answer)
    return {"message": "Answer posted successfully"}



