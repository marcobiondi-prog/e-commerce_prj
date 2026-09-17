from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.cart import CartItem
from app.schemas.cart import CartItemCreate


class CartService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_item(self, user_id: int, data: CartItemCreate) -> CartItem:
        stmt = select(CartItem).where(
            CartItem.user_id == user_id, CartItem.product_id == data.product_id
        )
        existing = (await self.db.execute(stmt)).scalar_one_or_none()
        if existing:
            existing.quantity += data.quantity
            return existing

        item = CartItem(user_id=user_id, product_id=data.product_id, quantity=data.quantity)
        self.db.add(item)
        await self.db.flush()
        return item

    async def list_items(self, user_id: int) -> list[CartItem]:
        stmt = select(CartItem).where(CartItem.user_id == user_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
