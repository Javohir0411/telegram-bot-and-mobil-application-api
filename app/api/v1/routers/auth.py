from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.db.schemas import (
    LoginRequest,
    UserResponse,
    UserBaseModel
)
from services.auth_user import (
    login_user,
    register_user
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register(data: UserBaseModel, db: AsyncSession = Depends(get_db)):
    return await register_user(db, data)


@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await login_user(data, db)
