from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.models import User
from app.db.schemas import ProductResponse, RentResponse

# product_router = APIRouter(prefix="/rent", tags=["Rent Process"])


# @product_router.get("", response_model=RentResponse)
# async def read_rents(
#         db: AsyncSession,
#         current_user: User = Depends(get_current_user())
# ):
#     return get_rents(db, current_user)
