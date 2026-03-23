from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
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
    user = await create_user(db=db, user_data=data)
    return user


async def login_user(data, db):
    user = await get_user_by_phone(db, data)
    print(f"LOGIN USER: {user}")

    access_token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "tenant_id": user.tenant_id,
    }
