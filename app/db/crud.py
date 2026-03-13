from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Product
from app.db.schemas import ProductCreate


async def get_products_service(db: AsyncSession, tenant_id: int):
    result = await db.execute(
        select(Product).where(Product.tenant_id == tenant_id)
    )
    return result.scalars().all()


async def create_product_service(
    db: AsyncSession,
    product_data: ProductCreate,
    tenant_id: int,
):
    new_product = Product(
        **product_data.model_dump(),
        tenant_id=tenant_id,
    )

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product