from pydoc import locate

from sqlalchemy_utils import database_exists, create_database

from app.infrastructure.persistence.database import engine

if not database_exists(engine.url):
    print("Creating new database", engine.name)
    create_database(engine.url)

metadata = locate("app.infrastructure.persistence.mappers.metadata")
