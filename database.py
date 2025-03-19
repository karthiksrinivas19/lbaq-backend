from pymongo import MongoClient
from models import User

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
    users_collection.insert_one(user_dict)

def get_user(name: str):
    """Retrieves a user from the MongoDB database by name."""
    user = users_collection.find_one({"name": name}, {"_id": 0})
    return user
