from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.record.record import Record
from app.domain.record.record_type import RecordType
from app.domain.user.user import User


class RecordLogic:
    @staticmethod
    def create(user: User, previous_record: Record, id: UUID = uuid4()) -> Record:
        now_utc = datetime.now(timezone.utc)
        return Record(
            id=id,
            user=user,
            type=RecordLogic.get_new_record_type(previous_record),
            ref_datetime=now_utc,
            ref_month=now_utc.month,
            ref_year=now_utc.year,
        )

    @staticmethod
    def get_new_record_type(previous_record: Record) -> RecordType:
        return RecordType.IN if previous_record.type is RecordType.OUT else RecordType.OUT
