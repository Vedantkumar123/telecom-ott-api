from datetime import datetime, timedelta
from app.repositories.subscription_repository import *
from app.repositories.plan_repository import *

def subscribe(user_id, plan_id):
    plan = get_plan_by_id(plan_id)

    if not plan:
        raise Exception("Plan not found")

    start = datetime.utcnow()
    end = start + timedelta(days=plan["validity_days"])

    data = {
        "user_id": user_id,
        "plan_id": plan_id,
        "start_date": start,
        "end_date": end,
        "status": "active"
    }

    create_subscription(data)
    return {"msg": "Subscribed successfully"}

def get_my_subscriptions(user_id):
    return get_user_subscriptions(user_id)