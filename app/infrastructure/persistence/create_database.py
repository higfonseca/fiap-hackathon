from pydoc import locate

from sqlalchemy_utils import create_database, database_exists

from app.infrastructure.persistence.database import engine  # type:ignore[attr-defined]

if not database_exists(engine.url):
    print("Creating new database", engine.name)
    create_database(engine.url)

metadata = locate("app.infrastructure.persistence.mappers.metadata")
