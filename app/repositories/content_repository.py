from app.core.database import db

def create_content(data):
    return db.content.insert_one(data)

def get_all_content():
    return list(db.content.find())

def get_content_by_id(content_id):
    from bson import ObjectId
    return db.content.find_one({"_id": ObjectId(content_id)})