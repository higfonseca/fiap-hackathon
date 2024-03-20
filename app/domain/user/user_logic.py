from uuid import UUID

from app.domain.user.user import User


class PersonLogic:
    @staticmethod
    def create(id: UUID, name: str, work_email: str) -> User:
        return User(
            id=id,
            name=name,
            work_email=work_email,
        )
