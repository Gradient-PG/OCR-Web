from pymongo import MongoClient
import os
import json
import base64

def get_db():
    """Return a database connection to MongoDB"""
    try:
        client = MongoClient(
            host=os.getenv("MONGO_HOST", "localhost"),
            port=int(os.getenv("MONGO_PORT", 27017)),
            username=os.getenv("MONGO_USER", "root"),
            password=os.getenv("MONGO_PASS", "pass"),
        )
        db = client["main_db"]
        return db
    except Exception as e:
        raise

def get_card_correctness(_id):
    db = get_db()
    collection = db['cards']

    card = collection.find_one({"_id": _id})

    if not card:
        return {"error": "Card not found."}

    return int(card["correct"])


def mark_checked(data):
    correct_num = get_card_correctness(data["_id"])
    data['correct'] = int(correct_num) + 1
    print(data)
    print(f"Marked as correct: {data}")


def mark_unchecked(data):
    data['correct'] = 0
