from fastapi import APIRouter, Depends
from app.schemas.content_schema import *
from app.services.content_service import *
from app.core.dependencies import admin_required, get_current_user

router = APIRouter(prefix="/content", tags=["Content"])

@router.get("/")
def browse_content(user=Depends(get_current_user)):
    return get_content()

@router.post("/")
def create(content: ContentCreate, user=Depends(admin_required)):
    return add_content(content)