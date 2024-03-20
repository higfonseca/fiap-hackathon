from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(kw_only=True, init=True)
class User:
    name: str
    work_email: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    deleted_at: datetime | None = field(default=None)
