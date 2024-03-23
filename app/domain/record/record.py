from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.record.record_type import RecordType
from app.domain.user.user import User


@dataclass
class Record:
    id: UUID
    user: User
    type: RecordType
    ref_datetime: datetime
    ref_month: int
    ref_year: int
