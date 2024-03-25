from datetime import datetime, timezone
from typing import Tuple
from uuid import UUID

from app.application.use_cases.record.get_records import GetRecords
from app.domain.shared.message_code import MessageCode
from app.infrastructure.persistence.repositories.user_postgres_repository import UserPostgresRepository
from app.infrastructure.services.notification_provider import NotificationProvider


class CreateReport:
    def __init__(
        self,
        get_records_usecase: GetRecords,
        notification_provider: NotificationProvider,
        user_repository: UserPostgresRepository,
    ):
        self.__get_records_usecase = get_records_usecase
        self.__notification_provider = notification_provider
        self.__user_repository = user_repository

    async def __call__(self, user_id: UUID) -> None:
        user = await self.__user_repository.find(user_id)

        this_month, this_year = self.__get_last_month_and_year()
        report_properties = await self.__get_records_usecase(user_id=user_id, ref_month=this_month, ref_year=this_year)

        self.__notification_provider.send_email(
            email=user.work_email, message_code=MessageCode.MONTH_REPORT, properties=report_properties.dict()
        )

    @staticmethod
    def __get_last_month_and_year() -> Tuple[int, int]:
        today = datetime.now(timezone.utc)
        return today.month, today.year
