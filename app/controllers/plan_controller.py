from fastapi import APIRouter, Depends
from app.schemas.plan_schema import *
from app.services.plan_service import *
from app.core.dependencies import admin_required

router = APIRouter(prefix="/plans", tags=["Plans"])

@router.get("/")
def get_plans():
    return get_plans_service()

@router.post("/")
def create_plan(plan: PlanCreate, user=Depends(admin_required)):
    return create_plan_service(plan)