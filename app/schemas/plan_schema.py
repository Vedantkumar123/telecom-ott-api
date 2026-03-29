from pydantic import BaseModel

class PlanCreate(BaseModel):
    name: str
    price: float
    validity_days: int
    included_apps: list[str]