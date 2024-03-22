from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from app.domain.records.record_type import RecordType
from app.domain.user.user import User


@dataclass
class Record:
    id: UUID
    user: User
    type: RecordType
    ref_datetime: datetime = field(default_factory=datetime.utcnow)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    deleted_at: datetime | None = field(default=None)
