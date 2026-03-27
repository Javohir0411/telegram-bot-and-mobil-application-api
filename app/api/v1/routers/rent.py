from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.core.session import get_db
from app.db.crud import get_rents, get_rent_by_id, create_rent, update_rent, delete_rent
from app.db.models import User
from app.db.schemas import RentResponse, RentCreate, RentUpdate

rent_router = APIRouter(prefix="/rent", tags=["Rent Process"])


@rent_router.get("", response_model=list[RentResponse])
async def read_rents(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await get_rents(db, current_user.id)


@rent_router.get("/{rent_id}", response_model=RentResponse)
async def read_rent(
        rent_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),

):
    return await get_rent_by_id(db, rent_id, current_user.id)


@rent_router.post("", response_model=RentResponse)
async def add_rent(
        rent_data: RentCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await create_rent(db, rent_data, current_user.id)


@rent_router.put("/{rent_id}", response_model=RentResponse)
async def modify_rent(
        rent_id: int,
        rent_data: RentUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await update_rent(db, rent_data, rent_id, current_user.id)


@rent_router.delete("/{rent_id}", response_model=RentResponse)
async def remove_rent(
        rent_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await delete_rent(db, rent_id, current_user.id)
