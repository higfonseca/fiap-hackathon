import os
from enum import Enum

from pydantic_settings import BaseSettings
from sqlalchemy import URL  # type:ignore[attr-defined]


class Environment(Enum):
    LOCAL = "local"
    TEST = "test"
    PRODUCTION = "production"


class Settings(BaseSettings):  # type: ignore[misc]
    app_name: str = "hackathon"
    environment: Environment = Environment(os.getenv("ENVIRONMENT", "production"))
    is_production: bool = environment is Environment.PRODUCTION

    database_host: str = os.getenv("POSTGRES_HOST") or "default"
    database_name: str = os.getenv("POSTGRES_DATABASE_NAME") or "default"
    database_port: str = os.getenv("POSTGRES_PORT") or "default"
    database_user: str = os.getenv("POSTGRES_USER") or "default"
    database_password: str = os.getenv("POSTGRES_PASSWORD") or "default"
    database_url: URL = URL.create(
        "postgresql",
        database=database_name,
        host=database_host,
        username=database_user,
        password=database_password,
    )

    @property
    def trusted_hosts(self) -> list[str]:
        hosts = [""]
        if self.environment is Environment.LOCAL or self.environment is Environment.TEST:
            hosts.append("localhost")

        return hosts


settings = Settings()
