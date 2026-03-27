from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.db.crud import delete_renter
from app.db.models import User
from app.db.schemas import (
    LoginRequest,
    UserResponse,
    UserBaseModel, UserUpdate
)
from services.auth_user import (
    login_user,
    register_user
)

router = APIRouter(prefix="/auth", tags=["User endpoints"])
auth_router = APIRouter(prefix="/auth", tags=["Authentication endpoints"])


@auth_router.post("/register", response_model=UserResponse)
async def register(data: UserBaseModel, db: AsyncSession = Depends(get_db)):
    return await register_user(db, data)


@auth_router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await login_user(data, db)


@auth_router.post("/logout")
async def logout():
    return {"message": "Logged out"}


@router.get("/user")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User)
    )
    return result.scalars().all()


@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Kiritilgan ID raqam egasi bazadan topilmadi")
    return user


@router.put("/{user_id}")
async def update_user(
        user_id: int,
        user_update: UserUpdate,
        db: AsyncSession = Depends(get_db), ):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Kiritlgan ID raqam egasi bazadan topilmadi"
        )
    if user_update.user_fullname:
        user.user_fullname = user_update.user_fullname
    if user_update.user_phone_number:
        user.user_phone_number = user_update.user_phone_number
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}", response_model=UserResponse)
async def remove_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Bu ID raqam egasi bazadan topilmadi"
        )
    user.is_active = False
    await db.commit()
    return user
