from typing import Optional
from pydantic import BaseModel
from app.utils.enums import ProductTypeEnum, ProductSizeEnum


# ______________ User Schemas _________________
class UserBaseModel(BaseModel):
    user_fullname: str
    user_phone_number: str
    selected_language: str
    password_hash: str
    is_active: str
    is_phone_verified: str


class UserResponse(BaseModel):
    id: int
    user_fullname: str
    user_phone_number: str


class LoginRequest(BaseModel):
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
    tenant_id: int
    product_type: ProductTypeEnum
    product_size: Optional[ProductSizeEnum] = None
    total_quantity: int
    price_per_day: Optional[float] = None

    class Config:
        from_attributes = True
