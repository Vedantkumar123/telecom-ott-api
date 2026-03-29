from app.core.database import db

def get_user_by_mobile(mobile):
    return db.users.find_one({"mobile_number": mobile})

def create_user(user_data):
    return db.users.insert_one(user_data)