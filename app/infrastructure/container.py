# pylint: disable=no-name-in-module
import logging

from dependency_injector.containers import DeclarativeContainer  # pylint: disable=no-name-in-module
from dependency_injector.providers import Configuration, Factory, Singleton

from app.application.use_cases.record.create_record import CreateRecord
from app.application.use_cases.user.authenticate_user import AuthenticateUser
from app.application.use_cases.record.get_records import GetRecords
from app.domain.record.services.worked_time_calculator import WorkedTimeCalculator
from app.infrastructure.persistence.database import SessionProvider  # type:ignore[attr-defined]
from app.infrastructure.persistence.mapping_configuration import import_mappers
from app.infrastructure.persistence.repositories.record_postgres_repository import RecordPostgresRepository
from app.infrastructure.persistence.repositories.user_postgres_repository import UserPostgresRepository


class ApplicationContainer(DeclarativeContainer):
    config = Configuration()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    import_mappers()
    session_provider = SessionProvider()

    # REPOSITORIES
    user_repository = Factory(UserPostgresRepository, database_session=session_provider)
    record_repository = Factory(RecordPostgresRepository, database_session=session_provider)

    # SERVICES
    worked_time_calculator = Singleton(WorkedTimeCalculator)

    # USE CASES
    create_record = Singleton(CreateRecord, user_repository=user_repository, record_repository=record_repository)
    get_records = Singleton(
        GetRecords, worked_time_calculator=worked_time_calculator, record_repository=record_repository
    )

    authenticate_user = Factory(AuthenticateUser, user_repository=user_repository)
