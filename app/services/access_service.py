from app.repositories.subscription_repository import get_active_subscription
from app.repositories.plan_repository import get_plan_by_id
from app.repositories.content_repository import get_content_by_id
from app.repositories.access_log_repository import *
from fastapi import HTTPException

def access_content(user_id, content_id):
    try:
        sub = get_active_subscription(user_id)

        if not sub:
            raise HTTPException(status_code=404, detail="No active subscription")

        plan = get_plan_by_id(sub["plan_id"])
        content = get_content_by_id(content_id)

        if content["platform"] not in plan["included_apps"]:
            raise HTTPException(status_code=403, detail="Content not allowed in your plan")

        result = log_access(user_id, content_id)
        return {"message": "Access granted", "log_id": str(result.inserted_id)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_access_history(user_id):
    try:
        history = get_history(user_id)
        for log in history:
            if "_id" in log:
                log["_id"] = str(log["_id"])
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))