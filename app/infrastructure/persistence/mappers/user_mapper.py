from datetime import datetime

from sqlalchemy import Column, DateTime, String, Table
from sqlalchemy.dialects.postgresql import UUID

from app.domain.user.user import User
from app.infrastructure.persistence.create_database import metadata
from app.infrastructure.persistence.mappers import mapper_registry

user_table = Table(
    "users",
    metadata,  # type:ignore[arg-type]
    Column("id", UUID, primary_key=True),
    Column("name", String(255), nullable=False),
    Column("work_email", String(255), nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
    Column("deleted_at", DateTime, default=None, nullable=True),
)

mapper_registry.map_imperatively(User, user_table)
