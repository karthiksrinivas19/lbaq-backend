from pymongo import MongoClient
from models import Query, User
from cryptography.fernet import Fernet
from app import SECRET_KEY

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

def add_user(user: User):
    """Adds a user to the MongoDB database."""
    user_dict = user.dict()
    if users_collection.find_one({"name": user.name}):
        raise ValueError("User already exists")
    cipher_suite = Fernet(SECRET_KEY)
    # Encrypt the password
    user_dict['password'] = cipher_suite.encrypt(user_dict['password'].encode()).decode()
    users_collection.insert_one(user_dict)

def get_user(name: str):
    """Retrieves a user from the MongoDB database by name."""
    user = users_collection.find_one({"name": name}, {"_id": 0})
    return user

def get_news():
    """Retrieves all news from the MongoDB database."""
    news = db.news.find({}, {"_id": 0})
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


def get_query_by_id(query_id: int):
    """Retrieves a query from the MongoDB database by ID."""
    query = db.queries.find_one({"query_id": query_id}, {"_id": 0})
    return query

def add_answer_to_query(query_id: int, answer: str, user_name: str):
    """Adds an answer to a query in the MongoDB database."""
    query = db.queries.find_one({"query_id": query_id})
    if not query:
        raise ValueError("Query not found")
    answer_dict = {
        "query_id": query_id,
        "answer": answer,
        "department": query["department"],
        "location": query["location"],
        "user_name": user_name
    }
    db.answers.insert_one(answer_dict)
    return "Answer added successfully"
