from pydantic import BaseModel

class UserCreate(BaseModel):
    mobile_number: str
    password: str

class UserLogin(BaseModel):
    mobile_number: str
    password: str