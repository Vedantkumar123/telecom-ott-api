from pydantic import BaseModel

class SubscriptionCreate(BaseModel):
    plan_id: str

class SubscriptionResponse(BaseModel):
    user_id: str
    plan_id: str
    status: str