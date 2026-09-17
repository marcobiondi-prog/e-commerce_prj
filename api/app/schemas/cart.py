from pydantic import BaseModel, ConfigDict

from app.schemas.product import ProductOut


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quantity: int
    product: ProductOut
