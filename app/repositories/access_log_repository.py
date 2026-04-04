from app.core.database import db
from datetime import datetime

def log_access(user_id, content_id):
    return db.access_logs.insert_one({
        "user_id": user_id,
        "content_id": content_id,
        "watched_at": datetime.utcnow()
    })

def get_history(user_id):
    return list(db.access_logs.find({"user_id": user_id}))