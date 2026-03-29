from app.repositories.subscription_repository import get_active_subscription
from app.repositories.plan_repository import get_plan_by_id
from app.repositories.content_repository import get_content_by_id
from app.repositories.access_log_repository import *

def access_content(user_id, content_id):
    sub = get_active_subscription(user_id)

    if not sub:
        raise Exception("No active subscription")

    plan = get_plan_by_id(sub["plan_id"])
    content = get_content_by_id(content_id)

    if content["platform"] not in plan["included_apps"]:
        raise Exception("Content not allowed in your plan")

    log_access(user_id, content_id)

    return {"msg": "Access granted"}

def get_access_history(user_id):
    return get_history(user_id)