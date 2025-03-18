from pymongo import MongoClient

MONGO_URL = "hello"

# Create a synchronous MongoDB client
client = MongoClient(MONGO_URL)
try:
	print("Databases:", client.list_database_names())
except Exception as e:
	print("Error listing databases:", e)

# Select the database
db = client.LBAQ

