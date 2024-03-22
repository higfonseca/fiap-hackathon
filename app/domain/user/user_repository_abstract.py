from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.user.user import User


class UserRepositoryAbstract(ABC):
    @abstractmethod
    async def save(self, user: User) -> None:
        pass

    @abstractmethod
    async def find(self, user_id: UUID) -> User:
        pass

    @abstractmethod
    async def find_by_work_email(self, work_email: str) -> User:
        pass
