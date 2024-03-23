from uuid import UUID

from app.domain.record.record_logic import RecordLogic
from app.domain.record.record_repository_abstract import RecordRepositoryAbstract
from app.domain.user.user_repository_abstract import UserRepositoryAbstract


class CreateRecord:
    def __init__(self, user_repository: UserRepositoryAbstract, record_repository: RecordRepositoryAbstract):
        self.__user_repository = user_repository
        self.__record_repository = record_repository

    async def __call__(self, user_id: UUID) -> None:
        user = await self.__user_repository.find(user_id)
        todays_previous_record = await self.__record_repository.get_user_todays_last_record(user_id)

        new_record = RecordLogic.create(user=user, todays_previous_record=todays_previous_record)
        await self.__record_repository.save(new_record)
