from pydantic import BaseModel
from typing import Optional

from app.utils.enums import ProductTypeEnum, ProductSizeEnum


class ProductBase(BaseModel):
    product_type: ProductTypeEnum
    product_size: Optional[ProductSizeEnum] = None
    total_quantity: int
    price_per_day: Optional[float] = None


class ProductResponse(ProductBase):
    id: int
    tenant_id: int

    class Config:
        from_attributes = True