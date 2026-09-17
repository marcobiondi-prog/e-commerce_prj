from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import cache_get, cache_set
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate


class ProductService:
    def __init__(self, db: AsyncSession):
        self.repo = ProductRepository(db)

    async def list_products(self, q: str | None, min_price: float | None, max_price: float | None):
        cache_key = f"products:{q}:{min_price}:{max_price}"
        cached = await cache_get(cache_key)
        if cached is not None:
            return cached

        products = await self.repo.list(q, min_price, max_price)
        result = [
            {
                "id": p.id, "name": p.name, "description": p.description,
                "price": float(p.price), "stock_quantity": p.stock_quantity,
                "image_url": p.image_url,
            }
            for p in products
        ]
        await cache_set(cache_key, result, ttl_seconds=120)
        return result

    async def create_product(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        return await self.repo.create(product)
