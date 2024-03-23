from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass(kw_only=True, init=True)
class User:
    id: UUID
    name: str
    work_email: str
    enrollment: str
    password: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    deleted_at: datetime | None = field(default=None)
