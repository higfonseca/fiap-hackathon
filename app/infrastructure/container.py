# pylint: disable=no-name-in-module
import logging

from dependency_injector.containers import DeclarativeContainer  # pylint: disable=no-name-in-module
from dependency_injector.providers import Configuration, Factory

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

    # PROVIDERS

    # USE CASES
