from dataclasses import dataclass
from uuid import UUID

from app.domain.payment.card_details import CardDetails
from app.domain.payment.payment_method import PaymentMethod


@dataclass(kw_only=True, init=True)
class MakePaymentDto:
    order_id: UUID
    customer_id: UUID
    total_price: float
    payment_method: PaymentMethod
    card_details: CardDetails
