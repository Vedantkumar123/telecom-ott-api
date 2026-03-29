from fastapi import APIRouter, Depends
from app.schemas.subscription_schema import *
from app.services.subscription_service import *
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

@router.post("/")
def subscribe_plan(sub: SubscriptionCreate, user=Depends(get_current_user)):
    return subscribe(user["user_id"], sub.plan_id)

@router.get("/my")
def my_subscriptions(user=Depends(get_current_user)):
    return get_my_subscriptions(user["user_id"])