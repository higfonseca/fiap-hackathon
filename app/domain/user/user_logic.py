from uuid import UUID, uuid4

from app.domain.user.user import User


class UserLogic:
    @staticmethod
    def create(name: str, work_email: str, enrollment: str, password: str, id: UUID = uuid4()) -> User:
        return User(id=id, name=name, work_email=work_email, enrollment=enrollment, password=password)
