from datetime import date
from typing import Optional
from pydantic import BaseModel
from app.utils.enums import ProductTypeEnum, ProductSizeEnum, PaymentStatusEnum, RentStatusEnum


# ______________ User Schemas _________________
class UserBaseModel(BaseModel):
    user_fullname: str
    user_phone_number: str
    selected_language: str
    password_hash: str
    is_active: str
    is_phone_verified: str
    warehouse_latitude: float
    warehouse_longitude: float


class UserResponse(BaseModel):
    id: int
    user_fullname: str
    user_phone_number: str


class UserUpdate(BaseModel):
    user_fullname: str
    user_phone_number: str


class LoginRequest(BaseModel):
    user_phone_number: str
    password_hash: str


class LoginResponse(BaseModel):
    token: str
    token_type: str


# ______________ Product Schemas _________________

class ProductCreate(BaseModel):
    product_type: ProductTypeEnum
    product_size: Optional[ProductSizeEnum] = None
    total_quantity: int
    price_per_day: Optional[float] = None


class ProductResponse(BaseModel):
    id: int
    user_id: int
    product_type: ProductTypeEnum
    product_size: Optional[ProductSizeEnum] = None
    total_quantity: int
    price_per_day: Optional[float] = None

    class Config:
        from_attributes = True


# ______________ Rent Schemas _________________


class RenterBase(BaseModel):
    renter_fullname: str
    renter_phone_number: str
    renter_passport_info: str | None = None


class RenterCreate(RenterBase):
    pass


class RenterUpdate(BaseModel):
    renter_fullname: str | None = None
    renter_phone_number: str | None = None
    renter_passport_info: str | None = None


class RenterResponse(RenterBase):
    id: int
    is_active: bool | None = None

    class Config:
        from_attributes = True


# ______________ Rent Schemas _________________

class RentBase(BaseModel):
    renter_id: int
    product_id: int

    quantity: int
    returned_quantity: int = 0

    start_date: date
    end_date: date | None = None

    latitude: float | None = None
    longitude: float | None = None

    delivery_needed: bool = False
    delivery_price: float | None = None

    product_price: float | None = None
    rent_price: float | None = None

    comment: str


class RentCreate(RentBase):
    pass


class RentUpdate(BaseModel):
    quantity: int | None = None
    start_date: date | None = None
    end_date: date | None = None

    delivery_needed: bool | None = None
    delivery_price: float | None = None

    rent_price: float | None = None
    comment: str | None = None


class RentReturnUpdate(BaseModel):
    returned_quantity: int


class RentStatusUpdate(BaseModel):
    rent_status: RentStatusEnum


class PaymentUpdate(BaseModel):
    status: PaymentStatusEnum


class RentResponse(RentBase):
    id: int
    user_id: int

    product: ProductResponse
    renter: RenterResponse

    class Config:
        from_attributes = True  # (Pydantic v2)
