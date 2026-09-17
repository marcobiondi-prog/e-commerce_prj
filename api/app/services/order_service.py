from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order, OrderItem
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.services.cart_service import CartService
from app.services.payment import get_payment_strategy
from app.tasks.email_tasks import send_order_confirmation


class OrderService:
    """Orchestra carrello, stock, pagamento e persistenza ordine in
    un'unica transazione (Unit of Work) e delega gli effetti collaterali
    lenti (email) a Celery, fuori dal ciclo richiesta-risposta."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.product_repo = ProductRepository(db)
        self.cart_service = CartService(db)

    async def checkout(self, user_id: int, payment_provider: str = "stripe") -> Order:
        cart_items = await self.cart_service.list_items(user_id)
        if not cart_items:
            raise ValueError("Cart is empty")

        order_items = []
        total = 0.0
        for item in cart_items:
            product = await self.product_repo.get_by_id(item.product_id)
            await self.product_repo.decrement_stock(item.product_id, item.quantity)
            unit_price = float(product.price)
            total += unit_price * item.quantity
            order_items.append(
                OrderItem(product_id=product.id, quantity=item.quantity, unit_price=unit_price)
            )

        order = Order(user_id=user_id, status="paid", total_amount=total, items=order_items)
        order = await self.order_repo.create(order)

        payment = get_payment_strategy(payment_provider)
        payment.charge(total, order.id)

        for item in cart_items:
            await self.db.delete(item)

        send_order_confirmation.delay(order.id)

        return order
