from fastapi import APIRouter
from app.api.v1.routers.products import product_router
from app.api.v1.routers.auth import router as auth_router
from app.api.v1.routers.renter import router as renter_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(product_router)
router.include_router(renter_router)