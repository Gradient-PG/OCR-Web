import datetime

from bcrypt import checkpw
from app.core.db import get_db


def user_exists(login):
    db = get_db()
    collection = db['users']
    user = collection.find_one({"login": login})
    if user is not None:
        return True
    else:
        return False


def password_correct(login, password):
    db = get_db()
    collection = db['users']
    user = collection.find_one({"login": login})

    if checkpw(password.encode('utf-8'), user['password']):
        return True
    else:
        return False

def has_password_expired(login):
    db = get_db()
    collection = db['users']
    user = collection.find_one({"login": login})

    if user['is_super_user']:
        return False

    user_created_at = user['created_at']

    current_time = datetime.datetime.now()
    time_difference = current_time - user_created_at

    if time_difference >= datetime.timedelta(hours=4):
        collection.update_one(
            {"login": login},
            {"$unset": {"password": ""}})
        return True
    else:
        return False

def is_admin(login):
    db = get_db()
    collection = db['users']
    user = collection.find_one({"login": login})

    return user is not None and user.get('is_super_user', False)