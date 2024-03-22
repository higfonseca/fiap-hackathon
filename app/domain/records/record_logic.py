from uuid import UUID, uuid4

from app.domain.records.record import Record
from app.domain.records.record_type import RecordType
from app.domain.user.user import User


class RecordLogic:
    @staticmethod
    def create(user: User, previous_record: Record, id: UUID = uuid4()) -> Record:
        return Record(id=id, user=user, type=RecordLogic.get_new_record_type(previous_record))

    @staticmethod
    def get_new_record_type(previous_record: Record) -> RecordType:
        return RecordType.IN if previous_record.type is RecordType.OUT else RecordType.OUT
