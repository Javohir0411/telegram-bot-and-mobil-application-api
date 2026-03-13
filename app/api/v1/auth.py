from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.core.security import create_access_token
from app.db.models import User


router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    user_phone_number: str


@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.user_phone_number == data.user_phone_number)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User topilmadi")

    access_token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "tenant_id": user.tenant_id,
    }