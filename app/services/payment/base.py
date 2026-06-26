from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def create_customer(self, email: str, name: str = None) -> str:
        pass

    @abstractmethod
    def create_checkout_session(self, customer_id: str, price_id: str, success_url: str, cancel_url: str) -> str:
        pass
