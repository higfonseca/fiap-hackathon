from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from pytest import fixture

from app.infrastructure.container import ApplicationContainer
from app.infrastructure.persistence.create_database import metadata
from app.presentation.startup import get_app


@fixture(autouse=True, scope="session")
def handle_test_database_and_migrate():
    command.upgrade(Config("alembic.ini"), "head")
    yield


@fixture(autouse=True, scope="function")
def api_client(request):
    app = get_app()
    client = TestClient(app, base_url="http://localhost")

    request.cls.client = client

    yield


@fixture(autouse=True)
def truncate_db_after_test():
    session = ApplicationContainer.session_provider()
    session.begin()

    try:
        yield
    except Exception:
        pass
    finally:
        for table in reversed(metadata.sorted_tables):
            session.execute(table.delete())

        session.commit()
        session.close()
