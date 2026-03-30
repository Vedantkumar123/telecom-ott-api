from pydantic import BaseModel

class UserCreate(BaseModel):
    mobile_number: str
    password: str
    role: str = "customer"

class UserLogin(BaseModel):
    mobile_number: str
    password: str