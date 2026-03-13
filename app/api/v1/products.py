from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import get_db
from app.core.security import get_current_user
from app.db.models import User
from app.db.schemas import ProductCreate, ProductResponse
from app.db.crud import get_products_service, create_product_service


product_router = APIRouter(prefix="/products", tags=["products"])


@product_router.get("", response_model=list[ProductResponse])
async def get_products(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_products_service(db, current_user.tenant_id)


@product_router.post("", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_product_service(db, product, current_user.tenant_id)