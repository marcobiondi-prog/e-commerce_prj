from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.product import ProductCreate, ProductOut
from app.services.product_service import ProductService

router = APIRouter()


@router.get("/", response_model=list[dict])
async def list_products(
    q: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await ProductService(db).list_products(q, min_price, max_price)


@router.post("/", response_model=ProductOut, status_code=201)
async def create_product(data: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await ProductService(db).create_product(data)
