from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.security import hash_password
from app.db.models import Product, User
from app.db.schemas import ProductCreate
from app.utils.get_product_by_id import product_by_id


# ---------- USER CRUD ------------------

# __________ USER Create _________________

async def create_user(db: AsyncSession, user_data):
    new_user = User(
        user_fullname=user_data.user_fullname,
        user_phone_number=user_data.user_phone_number,
        selected_language=user_data.selected_language,
        password_hash=hash_password(user_data.password_hash)  # eng muhumi shu
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# -----------PRODUCT CRUD -----------------

# __________ PRODUCT Read _________________

async def get_products(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Product).where(Product.user_id == user_id)
    )
    return result.scalars().all()


# __________ PRODUCT Read By id ________________

async def get_product_by_id(db: AsyncSession, product_id: int, user_id: int):
    result = await db.execute(
        select(Product).where(
            Product.id == product_id,
            Product.user_id == user_id
        )
    )
    return result.scalars().first()


# __________ PRODUCT Create ________________

async def create_product(
        db: AsyncSession,
        product_data: ProductCreate,
        user_id: int,
):
    new_product = Product(
        **product_data.model_dump(),
        user_id=user_id,
    )

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


# __________ PRODUCT Update ________________

async def update_product(db: AsyncSession, product_id: int, update_data, current_user_id: int):
    product = await product_by_id(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    if product.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't update a book"
        )
    if update_data.product_type is not None:
        product.product_type = update_data.product_type

    if update_data.product_size is not None:
        product.product_size = update_data.product_size

    if update_data.total_quantity is not None:
        product.total_quantity = update_data.total_quantity

    if update_data.price_per_day is not None:
        product.price_per_day = update_data.price_per_day

    await db.commit()
    await db.refresh(product)

    return product


# __________ PRODUCT Delete ________________

async def delete_product(db: AsyncSession, product_id: int, user_id: int):
    product = await product_by_id(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mahsulot topilmadi"
        )

    if product.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Siz bu mahsulotni o'chirishga ruxsatga ega emassiz"
        )
    await db.delete(product)
    await db.commit()
    return product
