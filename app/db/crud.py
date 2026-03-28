from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password
from fastapi import HTTPException
from sqlalchemy import select
from starlette import status
from app.db.models import (
    Product,
    User,
    Renter,
    Rent
)
from app.db.schemas import (
    ProductCreate,
    RenterCreate,
    RenterUpdate,
    RentCreate,
    RentUpdate
)
from app.utils.enums import PaymentStatusEnum, RentStatusEnum
from app.utils.get_product_by_id import product_by_id
from app.utils.get_renters import (
    get_renters_service,
    get_renter_by_id_service
)


# ----------   USER CRUD   ---------------
# ----------  PRODUCT CRUD ---------------
# ----------  RENTERS CRUD ---------------
# ----------   RENTS CRUD  ---------------


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
            detail="You can't update this product"
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


# -----------RENTERS CRUD -----------------

# __________ RENTER Read All _________________

async def get_renters(db: AsyncSession, user_id: int):
    renters = await get_renters_service(db, user_id)
    if renters is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sizning ijarachilaringiz topilmadi"
        )
    return renters


# __________ RENTER Read by id _________________

async def get_renters_by_id(db: AsyncSession, renter_id: int, user_id: int):
    renter = await get_renter_by_id_service(db, renter_id)
    if renter is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bu id raqamga ega ijarachi topilmadi"
        )
    if renter.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu id raqam egasi ma'lumotlari siz uchun emas ! "
        )
    return renter


# __________ RENTER Create _________________

async def create_renter(db: AsyncSession, renter_data: RenterCreate, user_id: int):
    new_renter = Renter(
        **renter_data.model_dump(),
        user_id=user_id
    )
    db.add(new_renter)
    await db.commit()
    await db.refresh(new_renter)
    return new_renter


# __________ RENTER Update _________________

async def update_renter(
        db: AsyncSession, renter_id: int, renter_data: RenterUpdate, user_id: int
):
    renter = await get_renter_by_id_service(db, renter_id)
    if not renter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bu id raqamga ega ijarachi topilmadi"
        )
    if renter.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Siz bu ijarachi ma'lumotlarini yangilay olmaysiz"
        )
    if renter_data.renter_fullname is not None:
        renter.renter_fullname = renter_data.renter_fullname

    if renter_data.renter_phone_number is not None:
        renter.renter_phone_number = renter_data.renter_phone_number

    if renter_data.renter_passport_info is not None:
        renter.renter_passport_info = renter_data.renter_passport_info
    await db.commit()
    await db.refresh(renter)

    return renter


# __________ RENTER Delete _________________

async def delete_renter(db: AsyncSession, renter_id: int, user_id: int):
    renter = await get_renter_by_id_service(db, renter_id)
    if not renter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Siz kiritgan id bo'yicha ijarachi topilmadi"
        )

    if renter.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu ID egasini ma'lumotlarini o'chira olmaysiz"
        )
    stmt = select(Rent).where(Rent.renter_id == renter_id)
    result = await db.execute(stmt)

    if result.scalars().first():
        renter.renter_is_active = False
        await db.commit()
        # return {"message": "Renter deactivated"}

    await db.delete(renter)
    await db.commit()
    return renter


# -----------RENTS CRUD -----------------

# __________ RENT Read All _________________

async def get_rents(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Rent).where(User.id == user_id)
    )
    rent = result.scalars().all()
    if not rent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ijaralar topilmadi !"
        )
    return rent


# __________ RENT Read By ID _________________

async def get_rent_by_id(db: AsyncSession, rent_id: int, user_id: int):
    result = await db.execute(
        select(Rent).where(
            Rent.id == rent_id,
            Rent.user_id == user_id,
        )
    )
    rent = result.scalars().first()
    if not rent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kiritilgan ID uchun ijara topilmadi !"
        )


# __________ RENT Create _________________

async def create_rent(
        db: AsyncSession, rent_data: RentCreate, user_id: int
):
    result = await db.execute(
        select(Product).where(Product.id == rent_data.product_id)
    )
    product = result.scalars().first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ijaraga bermoqchi bo'lgan mahsulotingiz bazadan topilmadi !"
        )
    if rent_data.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ijaraga beriladigan mahsulot miqdori 0 dan ko'p bo'lishi kerak"
        )
    if rent_data.quantity > product.total_quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kiritilgan miqdor bazadagi umumiy miqdordan oshib ketti"
        )
    if rent_data.end_date and rent_data.end_date < rent_data.start_date:
        raise HTTPException(400, "Tugash sana boshlanish sa")

    renter_result = await db.execute(
        select(Renter).where(
            Renter.renter_fullname == rent_data.renter_fullname,
            Renter.renter_phone_number == rent_data.renter_fullname,

        )
    )
    renter = renter_result.scalars().first()
    if not renter:
        renter = Renter(
            user_id=user_id,
            renter_fullname=rent_data.renter_fullname,
            renter_phone_number=rent_data.renter_fullname,
            renter_passport_info=rent_data.renter_passport_info,
        )
        db.add(renter)
        await db.flush()


# __________ RENT Update _________________

async def update_rent(
        db: AsyncSession, rent_id: int, rent_data: RentUpdate, user_id: int
):
    result = await db.execute(
        select(Rent).where(Rent.id == rent_id, Rent.user_id == user_id)
    )
    rent = result.scalars().first()
    if not rent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ijara topilmadi !"
        )
    update_data = rent_data.model_dump(exclude_unset=True)

    allowed_fields = {
        "quantity",
        "returned_quantity",
        "start_date",
        "end_date",
        "latitude",
        "longitude",
        "delivery_needed",
        "delivery_price",
        "product_price",
        "rent_price",
        "comment",
        "rent_status",
    }

    for key, value in update_data.items():
        if key in allowed_fields:
            setattr(rent, key, value)

    if rent.returned_quantity > rent.quantity:
        raise HTTPException(
            status_code=400,
            detail="Returned quantity cannot exceed quantity"
        )

    await db.commit()
    await db.refresh(rent)

    return rent


# __________ RENT Delete _________________

async def delete_rent(
        db: AsyncSession,
        rent_id: int,
        user_id: int,
):
    result = await db.execute(
        select(Rent).where(
            Rent.id == rent_id,
            Rent.user_id == user_id,
        )
    )
    rent = result.scalars().first()

    if not rent:
        raise HTTPException(status_code=404, detail="Rent not found")

    await db.delete(rent)
    await db.commit()
    return rent
