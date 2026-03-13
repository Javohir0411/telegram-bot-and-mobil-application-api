from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.security import get_current_user
from app.db.models import User


router = APIRouter(prefix="/users", tags=["users"])


class MeResponse(BaseModel):
    id: int
    tenant_id: int
    telegram_id: int
    user_fullname: str
    user_phone_number: str
    selected_language: str

    class Config:
        from_attributes = True


@router.get("/me", response_model=MeResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user