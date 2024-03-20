from dataclasses import dataclass

from app.domain.payment.payment_status import PaymentStatus


@dataclass(kw_only=True, init=True)
class UpdatePaymentStatusDto:
    payment_authorization_code: str
    new_status: PaymentStatus
