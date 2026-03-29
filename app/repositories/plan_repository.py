from app.core.database import db

def create_plan(plan):
    return db.plans.insert_one(plan)

def get_all_plans():
    return list(db.plans.find())
from bson import ObjectId
from app.core.database import db

def get_plan_by_id(plan_id):
    return db.plans.find_one({"_id": ObjectId(plan_id)})