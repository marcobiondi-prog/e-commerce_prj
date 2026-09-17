from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, order: Order) -> Order:
        self.db.add(order)
        await self.db.flush()
        return order

    async def list_for_user(self, user_id: int) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.items))
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
