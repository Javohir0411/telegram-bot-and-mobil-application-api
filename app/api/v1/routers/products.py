from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.core.dependencies import get_current_user
from app.db.models import User
from app.db.schemas import ProductCreate, ProductResponse, ProductUpdate
from app.db.crud import get_products, create_product, get_product_by_id, update_product, delete_product

product_router = APIRouter(prefix="/products", tags=["Products"])


@product_router.get("", response_model=list[ProductResponse])
async def read_products(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return await get_products(db, current_user.id)


@product_router.get("{product_id}")
async def read_product_by_id(
        product_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return await get_product_by_id(db, product_id, current_user.id)


@product_router.post("", response_model=ProductResponse)
async def add_product(
        product: ProductCreate,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    return await create_product(db, product, current_user.id)

@product_router.put("/{product_id}", response_model=ProductResponse)
async def modify_product(
        product_id: int,
        update_data: ProductUpdate,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    return await update_product(db, product_id, update_data, current_user.id)

@product_router.delete("/{product_id}", response_model=ProductResponse)
async def remove_product(
        product_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    return await delete_product(db, product_id, current_user.id)