from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.db.schemas import UserBaseModel


async def get_user_by_phone(db: AsyncSession, user: UserBaseModel):
    stmt = select(User).where(User.user_phone_number == user.user_phone_number)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
