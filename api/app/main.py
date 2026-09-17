from fastapi import FastAPI

from app.api.routes import auth, products, cart, orders

app = FastAPI(title="Ecommerce API", version="1.0.0")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])


@app.get("/health")
async def health_check():
    return {"status": "ok"}
