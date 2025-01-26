import datetime
import string
import random
import bcrypt
from app.core.db import get_db
from app import mail
from flask_mail import Message


def password_generator(length=10, symbols=False):
    characters = string.ascii_letters + string.digits
    if symbols:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def user_exists(data):
    db = get_db()
    collection = db['users']
    login = data['login']

    existing_user = collection.find_one({"login": login})
    return existing_user is not None


def create_user(data):
    db = get_db()
    collection = db['users']

    data['password'] = ''
    data['is_super_user'] = False
    data['created_at'] = datetime.datetime.now()
    collection.insert_one(data)

def generate_user_password(login):
    db = get_db()
    collection = db['users']
    user = collection.find_one({'login': login})

    if user is None:
        return False

    email = user['login']
    password = password_generator()

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    collection.update_one(
        {'login': login},
        {'$set': {'password': hashed_password, 'created_at': datetime.datetime.now()}}
    )

    send_password_mail(email, password)

    return True

def send_password_mail(email, password):
    msg = Message(
        subject='Hasło do konta w OCR-PCK.',
        sender='2eed70cdc0cea3',
        recipients=[email]
    )
    msg.body = f"""
                Szanowni Państwo,
                
                Witamy serdecznie w naszym programie! Dziękujemy za dołączenie i udział. Z radością informujemy, że hasło do Twojego konta zostało utworzone.
                
                Hasło: {password}
                
                Prosimy o zachowanie tego hasła w bezpiecznym miejscu. W razie jakichkolwiek pytań lub wątpliwości, prosimy o kontakt.
                
                Z poważaniem,
                Zespół OCR-PCK
                """

    mail.send(msg)