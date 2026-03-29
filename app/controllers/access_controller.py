from fastapi import APIRouter, Depends
from app.services.access_service import *
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/access", tags=["Access"])

@router.post("/{content_id}")
def access(content_id: str, user=Depends(get_current_user)):
    return access_content(user["user_id"], content_id)

@router.get("/history")
def history(user=Depends(get_current_user)):
    return get_access_history(user["user_id"])