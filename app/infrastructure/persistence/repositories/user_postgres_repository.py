import logging
from uuid import UUID

from sqlalchemy.exc import NoResultFound  # type:ignore[attr-defined]
from sqlalchemy.orm import Session

from app.domain.user.user import User
from app.domain.user.user_errors import UserErrors
from app.domain.user.user_repository_abstract import UserRepositoryAbstract


class UserPostgresRepository(UserRepositoryAbstract):
    def __init__(self, database_session: Session):
        self.__session = database_session

    async def save(self, user: User) -> None:
        try:
            self.__session.add(user)
            self.__session.commit()
        except Exception as err:
            logging.error(err)
            raise UserErrors.persist() from err

    async def find(self, user_id: UUID) -> User:
        try:
            return self.__session.query(User).filter(User.id == user_id).one()
        except NoResultFound as err:
            raise UserErrors.not_found() from err

    async def find_by_work_email(self, work_email: str) -> User:
        try:
            return self.__session.query(User).filter(User.work_email == work_email).one()
        except NoResultFound as err:
            raise UserErrors.not_found() from err
