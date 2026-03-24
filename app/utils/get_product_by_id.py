from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Product


async def product_by_id(db: AsyncSession, product_id: int):
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
