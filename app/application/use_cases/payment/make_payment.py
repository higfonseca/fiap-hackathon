from app.application.use_cases.payment.dtos.make_payment_dto import MakePaymentDto
from app.domain.payment.payment import Payment
from app.domain.payment.payment_provider_abstract import PaymentProviderAbstract, MakePaymentResponse
from app.domain.payment.payment_repository_abstract import PaymentRepositoryAbstract


class MakePayment:
    def __init__(self, payment_provider: PaymentProviderAbstract, payment_repository: PaymentRepositoryAbstract):
        self.__payment_provider = payment_provider
        self.__payment_repository = payment_repository

    async def __call__(self, dto: MakePaymentDto) -> None:
        payment_response = self.__payment_provider.make_payment(
            order_id=dto.order_id,
            total_price=dto.total_price,
            payment_method=dto.payment_method,
            card_details=dto.card_details,
        )

        payment = self.__build_payment(dto=dto, payment_response=payment_response)
        self.__payment_repository.save(payment)

    @staticmethod
    def __build_payment(dto: MakePaymentDto, payment_response: MakePaymentResponse) -> Payment:
        return Payment(
            order_id=dto.order_id,
            customer_id=dto.customer_id,
            total_price=dto.total_price,
            payment_method=dto.payment_method,
            provider_authorization_code=payment_response.authorization_code,
            status=payment_response.status,
        )
