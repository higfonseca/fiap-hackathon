import logging
from uuid import UUID

from sqlalchemy.exc import NoResultFound  # type:ignore[attr-defined]
from sqlalchemy.orm import Session

from app.domain.record.record import Record
from app.domain.record.record_errors import RecordErrors
from app.domain.record.record_repository_abstract import RecordRepositoryAbstract


class RecordPostgresRepository(RecordRepositoryAbstract):
    def __init__(self, database_session: Session):
        self.__session = database_session

    async def save(self, record: Record) -> None:
        try:
            self.__session.add(record)
            self.__session.commit()
        except Exception as err:
            logging.error(err)
            raise RecordErrors.persist() from err

    async def list_by_user(self, user_id: UUID) -> list[Record]:
        try:
            return self.__session.query(Record).filter(Record.user_id == user_id).all()  # type:ignore[attr-defined]
        except NoResultFound as _:
            return []

    async def list_by_user_month_and_year(self, user_id: UUID, ref_month: int, ref_year: int) -> list[Record]:
        try:
            return (
                self.__session.query(Record)
                .filter(
                    Record.user_id == user_id,  # type:ignore[attr-defined]
                    Record.ref_month == ref_month,
                    Record.ref_year == ref_year,
                )
                .all()
            )
        except NoResultFound as _:
            return []
