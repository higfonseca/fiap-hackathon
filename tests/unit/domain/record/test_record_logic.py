from unittest import TestCase

from freezegun import freeze_time

from app.domain.record.record_logic import RecordLogic
from app.domain.record.record_type import RecordType
from tests.factories.domain_factories import RecordFactory


@freeze_time("2024-03-23 10:00:00")
class TestRecordLogic(TestCase):
    def setUp(self) -> None:
        self.record = RecordFactory(type=RecordType.OUT)

    def test_create_WHEN_called_RETURNS_record(self):
        result = RecordLogic.create(
            user=self.record.user,
            previous_record=RecordFactory(type=RecordType.IN),
            id=self.record.id
        )
        self.assertEqual(self.record, result)

    def test_get_new_record_type_WHEN_previous_record_type_is_in_RETURNS_out(self):
        result = RecordLogic.get_new_record_type(RecordFactory(type=RecordType.IN))
        self.assertEqual(RecordType.OUT, result)

    def test_get_new_record_type_WHEN_previous_record_type_is_out_RETURNS_in(self):
        result = RecordLogic.get_new_record_type(RecordFactory(type=RecordType.OUT))
        self.assertEqual(RecordType.IN, result)
