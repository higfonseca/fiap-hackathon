# pylint: disable=no-name-in-module
import logging

from dependency_injector.containers import DeclarativeContainer  # pylint: disable=no-name-in-module
from dependency_injector.providers import Configuration

from app.infrastructure.persistence.database import SessionProvider
from app.infrastructure.persistence.mapping_configuration import import_mappers


class ApplicationContainer(DeclarativeContainer):
    config = Configuration()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    import_mappers()
    session_provider = SessionProvider()

    # REPOSITORIES

    # PROVIDERS

    # USE CASES
