from typing import Optional
from pydantic import BaseModel
from app.utils.enums import ProductTypeEnum, ProductSizeEnum


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