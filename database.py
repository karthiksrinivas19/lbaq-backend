from bson import ObjectId
from pymongo import MongoClient
from models import Query, User, Answer
from cryptography.fernet import Fernet
import hashlib
import hmac
SECRET_KEY="46gF9K-cXBZc742PSTNh-hoiJUqUgHNSTetng4WY6fA="

MONGO_URL = "mongodb+srv://karthik:1ypnL7u2hnIIFbvS@cluster1.bnv5i.mongodb.net/?retryWrites=true&w=majority"

# Create a synchronous MongoDB client
client = MongoClient(MONGO_URL)
try:
    print("Databases:", client.list_database_names())
except Exception as e:
    print("Error listing databases:", e)

# Select the database
db = client.LBAQ
users_collection = db.users  # Collection to store user data

def encode_password(password: str) -> str:
    return hmac.new(SECRET_KEY.encode(), password.encode(), hashlib.sha256).hexdigest()
    
def add_user(user: User):
    """Adds a user to the MongoDB database."""
    user_dict = user.dict()
    print("User data before insertion:", user_dict)  # Debugging line

    if users_collection.find_one({"name": user.name}):
        raise ValueError("User already exists")

    user_dict['password'] = encode_password(user.password)
    result = users_collection.insert_one(user_dict)
    print(f"User inserted with ID: {result.inserted_id}")  # Debugging line

def get_user(email: str):
    """Retrieves a user from the MongoDB database by email."""
    user = users_collection.find_one({"email": email}, {"_id": 0})
    return user

def get_news_by_location(location: str):
    """Retrieves news from the MongoDB database by location."""
    news = db.news.find({"location": location}, {"_id": 0})
    return list(news)

def add_query(query: Query):
    """Adds a query to the MongoDB database."""
    query_dict = query.dict()
    db.queries.insert_one(query_dict)

def add_news(news: dict):
    """Adds news to the MongoDB database."""
    db.news.insert_one(news)


def get_queries_by_location_and_department(location: str, department: str):
    """Retrieves queries from the MongoDB database by location and department."""  
    queries = db.queries.find({"location": location, "department": department}, {"_id": 0})
    return list(queries)


def get_query_by_id(query_id: str):
    return db.queries.find_one({"_id": ObjectId(query_id)})


def add_answer_to_query(answer:Answer):
    """Adds an answer to a query in the MongoDB database."""
    query = get_query_by_id(answer.query_id)
    print(query)
    if not query:
        raise ValueError("Query not found")
    answer_dict = answer.dict()
    db.answers.insert_one(answer_dict)
    return "Answer added successfully"