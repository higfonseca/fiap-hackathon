from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.record.record import Record
from app.domain.record.record_type import RecordType
from app.domain.user.user import User


class RecordLogic:
    @staticmethod
    def create(
        user: User,
        previous_record: Record | None = None,
        ref_datetime: datetime = datetime.now(timezone.utc),
        id: UUID = uuid4(),
    ) -> Record:
        return Record(
            id=id,
            user=user,
            type=RecordLogic.get_new_record_type(previous_record),
            ref_datetime=ref_datetime,
            ref_month=ref_datetime.month,
            ref_year=ref_datetime.year,
        )

    @staticmethod
    def get_new_record_type(previous_record: Record | None = None) -> RecordType:
        return RecordType.IN if previous_record is None or previous_record.type is RecordType.OUT else RecordType.OUT
