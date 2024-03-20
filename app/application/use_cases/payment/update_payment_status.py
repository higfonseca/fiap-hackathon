import logging
from uuid import UUID

from app.application.use_cases.payment.dtos.update_payment_status_dto import UpdatePaymentStatusDto
from app.domain.events.payment_updated_event import PaymentUpdatedEvent, PaymentUpdatedEventBody
from app.domain.payment.payment_logic import PaymentLogic
from app.domain.payment.payment_repository_abstract import PaymentRepositoryAbstract
from app.domain.payment.payment_status import PaymentStatus
from app.domain.shared.message_bus.message_bus_abstract import MessageBusAbstract


class UpdatePaymentStatus:
    def __init__(self, payment_repository: PaymentRepositoryAbstract, message_bus: MessageBusAbstract):
        self.__payment_repository = payment_repository
        self.__message_bus = message_bus

    async def __call__(self, dto: UpdatePaymentStatusDto) -> None:
        payment = self.__payment_repository.find_by_authorization_code(dto.payment_authorization_code)
        updated_payment = PaymentLogic.update_status(payment=payment, new_status=dto.new_status)
        self.__payment_repository.update(updated_payment)

        await self.__dispatch_event(order_id=payment.order_id, payment_status=dto.new_status)

    async def __dispatch_event(self, order_id: UUID, payment_status: PaymentStatus) -> None:
        logging.info("Payment for %s updated. Dispatching event", order_id)

        event = PaymentUpdatedEvent(  # pylint: disable=unexpected-keyword-arg
            body=PaymentUpdatedEventBody(order_id=order_id, status=payment_status)
        )
        await self.__message_bus.dispatch(event)
