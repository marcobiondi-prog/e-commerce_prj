from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product


class ProductRepository:
    """Isolates all SQL/ORM access for Product. The service layer never
    talks to SQLAlchemy directly (Repository pattern)."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, product_id: int) -> Product | None:
        return await self.db.get(Product, product_id)

    async def list(self, q: str | None = None, min_price: float | None = None,
                    max_price: float | None = None) -> list[Product]:
        stmt = select(Product)
        if q:
            stmt = stmt.where(Product.name.ilike(f"%{q}%"))
        if min_price is not None:
            stmt = stmt.where(Product.price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Product.price <= max_price)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, product: Product) -> Product:
        self.db.add(product)
        await self.db.flush()
        return product

    async def decrement_stock(self, product_id: int, quantity: int) -> None:
        product = await self.get_by_id(product_id)
        if product is None or product.stock_quantity < quantity:
            raise ValueError("Insufficient stock")
        product.stock_quantity -= quantity
