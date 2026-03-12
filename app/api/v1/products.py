from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.session import get_db
from app.db.crud import get_product_by_id_service, get_products_service
from app.db.models import Product

# from app.db.schemas import ProductResponse

product_router = APIRouter()


# - - - - - - - - - Products - - - - - - - - -

@product_router.get("/products")
async def get_products(db: AsyncSession = Depends(get_db)):
    return await get_products_service(db)


@product_router.get("/products/{product_id}")
async def get_product_by_id(product_id: int, db: AsyncSession = Depends(get_db)):
    return await get_product_by_id_service(db, product_id)
