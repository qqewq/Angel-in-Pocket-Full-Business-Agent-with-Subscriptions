import stripe
from .base import PaymentGateway
from ...config import settings

stripe.api_key = settings.stripe_secret_key

class StripeGateway(PaymentGateway):
    def create_customer(self, email: str, name: str = None) -> str:
        customer = stripe.Customer.create(email=email, name=name)
        return customer.id

    def create_checkout_session(self, customer_id: str, price_id: str, success_url: str, cancel_url: str) -> str:
        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session.url
