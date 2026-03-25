from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Renter


async def get_renters_service(db: AsyncSession, user_id: int):
    renters = await db.execute(
        select(Renter).where(Renter.user_id == user_id)
    )
    return renters.scalars().all()


async def get_renter_by_id_service(db: AsyncSession, renter_id: int):
    renter = await db.execute(
        select(Renter).where(
            Renter.id == renter_id
        )
    )
    return renter.scalars().first()
