# app/db/mongo.py

from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017"
MONGO_DB_NAME = "my_dataset_db"

client = MongoClient(MONGO_URL)
db = client[MONGO_DB_NAME]

def get_db():
    return db