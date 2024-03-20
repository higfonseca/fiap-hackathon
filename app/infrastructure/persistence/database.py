# type: ignore
import logging

from dependency_injector import providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.infrastructure.settings import settings

logger = logging.getLogger(__name__)
engine = create_engine(settings.database_url, pool_size=25, max_overflow=10)


class SessionProvider(providers.Provider):
    def __init__(self):
        super().__init__()
        self.session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=True))

    def _provide(self, *args, **kwargs):  # pylint: disable=unused-argument
        try:
            return self.session
        except Exception:
            logger.exception("Rolling back session due to raised exception")
            self.session.rollback()
            raise
        finally:
            self.session.close()

    @property
    def cls(self):
        return self.session.__class__
