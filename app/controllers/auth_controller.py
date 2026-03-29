from fastapi import APIRouter
from app.schemas.auth_schema import *
from app.services.auth_service import *

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register_user(user: UserCreate):
    return register(user)

@router.post("/login")
def login_user(user: UserLogin):
    return login(user)