from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.order import OrderOut
from app.services.order_service import OrderService

router = APIRouter()


@router.post("/checkout", response_model=OrderOut, status_code=201)
async def checkout(
    payment_provider: str = "stripe",
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await OrderService(db).checkout(user.id, payment_provider)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
