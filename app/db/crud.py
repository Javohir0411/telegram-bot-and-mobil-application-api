from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from app.db.models import Product


# - - - - - - - - - Products - - - - - - - - -


async def get_products_service(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()


async def get_product_by_id_service(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(Product)
        .where(Product.id == product_id)
    )
    return result.scalars().first()
