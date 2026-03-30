from app.repositories.plan_repository import *
from fastapi import HTTPException

def create_plan_service(plan):
    try:
        result = create_plan(plan.dict())
        return {"message": "Plan created successfully", "plan_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_plans_service():
    try:
        plans = get_all_plans()
        # Convert ObjectId to string for JSON serialization
        for plan in plans:
            plan['_id'] = str(plan['_id'])
        return plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))