from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
import hashlib
import hmac
from cryptography.fernet import Fernet
from mangum import Mangum

# Secret key for password encoding
SECRET_KEY = "46gF9K-cXBZc742PSTNh-hoiJUqUgHNSTetng4WY6fA="
MONGO_URL = "mongodb+srv://karthik:1ypnL7u2hnIIFbvS@cluster1.bnv5i.mongodb.net/?retryWrites=true&w=majority"

# Create a synchronous MongoDB client
client = MongoClient(MONGO_URL)
db = client.LBAQ

# Collections
users_collection = db.users
news_collection = db.news
queries_collection = db.queries
answers_collection = db.answers

app = FastAPI()

# Models
class User(BaseModel):
    name: str
    email: str
    password: str
    aadhar: str
    phone_number: str
    location: str
    is_officer: bool

class LoginData(BaseModel):
    email: str
    password: str

class News(BaseModel):
    email: str
    title: str
    description: str
    department: str
    location: str

class Query(BaseModel):
    email: str
    title: str
    description: str
    department: str
    location: str

class Answer(BaseModel):
    query_id: str
    email: str
    response: str

# Utility Functions
def encode_password(password: str) -> str:
    return hmac.new(SECRET_KEY.encode(), password.encode(), hashlib.sha256).hexdigest()

def get_user(email: str):
    return users_collection.find_one({"email": email}, {"_id": 0})

def add_user(user: User):
    if users_collection.find_one({"email": user.email}):
        raise ValueError("User already exists")
    user_dict = user.dict()
    user_dict["password"] = encode_password(user.password)
    users_collection.insert_one(user_dict)

def get_news_by_location(location: str):
    return list(news_collection.find({"location": location}, {"_id": 0}))

def add_news(news: dict):
    news_collection.insert_one(news)

def get_queries_by_location_and_department(location: str, department: str):
    return list(queries_collection.find({"location": location, "department": department}, {"_id": 0}))

def get_query_by_id(query_id: str):
    return queries_collection.find_one({"_id": ObjectId(query_id)})

def add_query(query: Query):
    queries_collection.insert_one(query.dict())

def add_answer_to_query(answer: Answer):
    if not get_query_by_id(answer.query_id):
        raise ValueError("Query not found")
    answers_collection.insert_one(answer.dict())

# API Endpoints
@app.get("/")
def index():
    return {"message": "Hello everyone"}

@app.post("/user/signup")
def signup(user: User):
    if get_user(user.email):
        raise HTTPException(status_code=400, detail="User already exists")
    add_user(user)
    return {"message": "User registered successfully"}

@app.post("/user/login")
def login(data: LoginData):
    user = get_user(data.email)
    if not user or user["password"] != encode_password(data.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful"}

@app.get("/user/{email}")
def fetch_user(email: str):
    user = get_user(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/news/{location}")
def fetch_news(location: str):
    news = get_news_by_location(location)
    if not news:
        raise HTTPException(status_code=404, detail="No news found")
    return news

@app.post("/add-news")
def post_news(news: News):
    user = get_user(news.email)
    if not user or not user["is_officer"]:
        raise HTTPException(status_code=403, detail="Only officers can post news")
    add_news(news.dict())
    return {"message": "News posted successfully"}

@app.post("/add-query")
def post_query(query: Query):
    if not get_user(query.email):
        raise HTTPException(status_code=404, detail="User not found")
    add_query(query)
    return {"message": "Query posted successfully"}

@app.get("/queries/{location}/{department}")
def fetch_queries(location: str, department: str):
    queries = get_queries_by_location_and_department(location, department)
    if not queries:
        raise HTTPException(status_code=404, detail="No queries found")
    return queries

@app.post("/queries/answer")
def post_answer(answer: Answer):
    user = get_user(answer.email)
    if not user or not user["is_officer"]:
        raise HTTPException(status_code=403, detail="Only officers can post answers")
    if not get_query_by_id(answer.query_id):
        raise HTTPException(status_code=404, detail="Query not found")
    add_answer_to_query(answer)
    return {"message": "Answer posted successfully"}

handler = Mangum(app)
