from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.domain.record.record import Record
from app.domain.record.record_type import RecordType
from app.domain.user.user import User
from app.infrastructure.persistence.create_database import metadata
from app.infrastructure.persistence.mappers import mapper_registry

record_table = Table(
    "records",
    metadata,  # type:ignore[arg-type]
    Column("id", UUID, primary_key=True),
    Column("user_id", ForeignKey("users.id", ondelete="cascade"), index=True),
    Column("type", Enum(RecordType), nullable=False),
    Column("ref_month", Integer(), nullable=False, index=True),
    Column("ref_year", Integer(), nullable=False, index=True),
    Column("ref_datetime", DateTime, default=datetime.utcnow),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
    Column("deleted_at", DateTime, default=None, nullable=True),
)

mapper_registry.map_imperatively(Record, record_table, properties={"user": relationship(User, backref="users")})
