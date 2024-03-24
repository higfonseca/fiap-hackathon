from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.record.record import Record


class RecordRepositoryAbstract(ABC):
    @abstractmethod
    async def save(self, record: Record) -> None:
        pass

    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> list[Record]:
        pass

    @abstractmethod
    async def list_by_user_month_and_year(self, user_id: UUID, ref_month: int, ref_year: int) -> list[Record]:
        pass

    @abstractmethod
    async def get_user_todays_last_record(self, user_id: UUID) -> Record | None:
        pass
