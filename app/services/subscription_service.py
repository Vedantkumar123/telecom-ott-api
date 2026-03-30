from datetime import datetime, timedelta
from app.repositories.subscription_repository import *
from app.repositories.plan_repository import *
from fastapi import HTTPException
from bson import ObjectId

def subscribe(user_id, plan_id):
    try:
        # Validate plan_id format
        try:
            ObjectId(plan_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid plan_id format. Must be a valid MongoDB ObjectId")
        
        plan = get_plan_by_id(plan_id)

        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")

        start = datetime.utcnow()
        end = start + timedelta(days=plan["validity_days"])

        data = {
            "user_id": user_id,
            "plan_id": plan_id,
            "start_date": start,
            "end_date": end,
            "status": "active"
        }

        result = create_subscription(data)
        return {"message": "Subscribed successfully", "subscription_id": str(result.inserted_id)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_my_subscriptions(user_id):
    try:
        subscriptions = get_user_subscriptions(user_id)
        for sub in subscriptions:
            if "_id" in sub:
                sub["_id"] = str(sub["_id"])
            if "plan_id" in sub:
                sub["plan_id"] = str(sub["plan_id"])
        return subscriptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))