from fastapi import APIRouter
from app.api.v1.routers.products import product_router as products_router
from app.api.v1.routers.auth import router as user_router
from app.api.v1.routers.auth import auth_router
from app.api.v1.routers.renter import router as renter_router
from app.api.v1.routers.rent import rent_router as rent_router

router = APIRouter()

router.include_router(products_router)
router.include_router(renter_router)
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(rent_router)
