from fastapi import APIRouter
from .products import product_router as products_router

router = APIRouter()

router.include_router(products_router)