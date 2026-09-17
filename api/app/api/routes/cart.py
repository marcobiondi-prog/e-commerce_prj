from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemOut
from app.services.cart_service import CartService

router = APIRouter()


@router.post("/items", response_model=CartItemOut, status_code=201)
async def add_to_cart(
    data: CartItemCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await CartService(db).add_item(user.id, data)


@router.get("/items", response_model=list[CartItemOut])
async def list_cart(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await CartService(db).list_items(user.id)
