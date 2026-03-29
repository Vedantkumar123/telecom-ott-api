from app.repositories.plan_repository import *

def create_plan_service(plan):
    return create_plan(plan.dict())

def get_plans_service():
    return get_all_plans()