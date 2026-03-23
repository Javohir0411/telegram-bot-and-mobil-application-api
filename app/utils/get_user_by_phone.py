from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.db.schemas import UserBaseModel


async def get_user_by_phone(db: AsyncSession, user: UserBaseModel):
    result = await db.execute(
        select(User).where(User.user_phone_number == user.user_phone_number)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User topilmadi")
    return user
