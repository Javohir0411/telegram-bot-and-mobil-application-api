from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password
from app.db.crud import create_user
from app.db.models import User
from app.db.schemas import UserBaseModel
from app.utils.get_user_by_phone import get_user_by_phone


async def register_user(db: AsyncSession, data: UserBaseModel):
    user = await get_user_by_phone(db=db, user=data)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu telefon raqam bilan foydalanuvchi allaqachon mavjud"
        )
    result = await create_user(db=db, user_data=data)
    return result


async def login_user(data, db):
    user = await get_user_by_phone(db, data)
    print(f"LOGIN USER: {user}")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Telefon raqam yoki password xato !"
        )
    if not verify_password(data.password_hash, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Telefon raqam yoki password xato !"
        )

    access_token = create_access_token({"user_id": user.id, "user_phone_number": user.user_phone_number})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user.id,
            "user_full_name": user.user_fullname,
            "user_phone_number": user.user_phone_number,

        }
    }
