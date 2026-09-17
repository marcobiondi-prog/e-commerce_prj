from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    """Strategy pattern: each payment provider implements the same
    interface, so OrderService doesn't need to know which one is used."""

    @abstractmethod
    def charge(self, amount: float, order_id: int) -> str:
        """Returns a provider transaction id."""


class StripePayment(PaymentStrategy):
    def charge(self, amount: float, order_id: int) -> str:
        # chiamata reale all'SDK Stripe qui
        return f"stripe_tx_{order_id}"


class PaypalPayment(PaymentStrategy):
    def charge(self, amount: float, order_id: int) -> str:
        # chiamata reale all'SDK PayPal qui
        return f"paypal_tx_{order_id}"


def get_payment_strategy(provider: str) -> PaymentStrategy:
    strategies = {"stripe": StripePayment, "paypal": PaypalPayment}
    if provider not in strategies:
        raise ValueError(f"Unknown payment provider: {provider}")
    return strategies[provider]()
