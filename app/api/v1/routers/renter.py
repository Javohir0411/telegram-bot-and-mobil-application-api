from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.core.session import get_db
from app.db.crud import get_renters, get_renters_by_id, create_renter, update_product, delete_renter, update_renter
from app.db.models import User
from app.db.schemas import RenterResponse, RenterCreate, RenterUpdate

router = APIRouter(prefix="/renter", tags=["Renters"])


@router.get("", response_model=list[RenterResponse])
async def read_rents(
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await get_renters(db, user.id)


@router.get("{renter_id}", response_model=RenterResponse)
async def read_rent_by_id(
        renter_id: int,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await get_renters_by_id(db, renter_id, user.id)


@router.post("", response_model=RenterResponse)
async def add_renter(
        renter_data: RenterCreate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await create_renter(db, renter_data, user.id)


@router.put("/{renter_id}", response_model=RenterResponse)
async def modify_renter(
        renter_id: int,
        renter_data: RenterUpdate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await update_renter(db, renter_id, renter_data, user.id)


@router.delete("/{renter_id}", response_model=RenterResponse)
async def remove_renter(
        renter_id: int,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await delete_renter(db, renter_id, user.id)
