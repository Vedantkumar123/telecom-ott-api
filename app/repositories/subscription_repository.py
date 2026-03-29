from app.core.database import db
from datetime import datetime

def create_subscription(data):
    return db.subscriptions.insert_one(data)

def get_user_subscriptions(user_id):
    return list(db.subscriptions.find({"user_id": user_id}))

def get_active_subscription(user_id):
    return db.subscriptions.find_one({
        "user_id": user_id,
        "status": "active"
    })