from datetime import datetime, time, timezone
from unittest import TestCase

from app.domain.record.enums import RecordType
from app.domain.record.record import Record
from app.domain.record.services.worked_time_calculator import WorkedTimeCalculator
from tests.factories.domain_factories import UserFactory, RecordFactory


class TestWorkedTimeCalculator(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

    def test_get_worked_time_by_date_WHEN_called_RETURNS_dict_with_dates_and_total_worked_time(self):
        records = self.__get_complete_records_list()
        result = WorkedTimeCalculator().calculate(records)

        expected_result = {
            datetime(2024, 3, 21).date(): time(7, 30),
            datetime(2024, 3, 22).date(): time(5, 30),
        }
        self.assertEqual(expected_result, result)

    def test_get_worked_time_by_date_WHEN_user_did_not_clock_out_RETURNS_worked_time_considering_exist_at_6_pm(self):
        records = self.__get_records_with_gaps()
        result = WorkedTimeCalculator().calculate(records)

        expected_result = {
            datetime(2024, 3, 21).date(): time(7, 30),
            datetime(2024, 3, 22).date(): time(6),
        }
        self.assertEqual(expected_result, result)

    def test_get_records_with_missing_clock_outs_WHEN_called_RETURNS_records_by_date_with_missing_clock_outs(self):
        records = self.__get_records_with_gaps()
        result = WorkedTimeCalculator().get_records_with_missing_clock_outs(records)
        times_by_date = {date: [rec.ref_datetime.time() for rec in recs] for date, recs in result.items()}

        expected_result = {
            datetime(2024, 3, 21).date(): [
                time(18, 0),
                time(13, 30),
                time(12, 0),
                time(9, 0)
            ],
            datetime(2024, 3, 22).date(): [
                time(18, 0),
                time(12, 0)
            ]
        }
        self.assertEqual(expected_result, times_by_date)

    def test_sum_worked_time_WHEN_called_RETURNS_worked_time(self):
        records = self.__get_records_with_gaps()
        records_by_date = WorkedTimeCalculator().get_records_with_missing_clock_outs(records)
        result = {date: WorkedTimeCalculator.sum_worked_time(recs) for date, recs in records_by_date.items()}

        expected_result = {
            datetime(2024, 3, 21).date(): time(7, 30),
            datetime(2024, 3, 22).date(): time(6),
        }
        self.assertEqual(expected_result, result)

    def __get_complete_records_list(self) -> list[Record]:
        record1 = RecordFactory(
            ref_datetime=datetime(2024, 3, 21, 9, 0).replace(tzinfo=timezone.utc),
            type=RecordType.IN,
            user=self.user,
        )
        record2 = RecordFactory(
            ref_datetime=datetime(2024, 3, 21, 12, 0).replace(tzinfo=timezone.utc),
            type=RecordType.OUT,
            user=self.user,
        )
        record3 = RecordFactory(
            ref_datetime=datetime(2024, 3, 21, 13, 30).replace(tzinfo=timezone.utc),
            type=RecordType.IN,
            user=self.user,
        )
        record4 = RecordFactory(
            ref_datetime=datetime(2024, 3, 21, 18, 0).replace(tzinfo=timezone.utc),
            type=RecordType.OUT,
            user=self.user,
        )

        record5 = RecordFactory(
            ref_datetime=datetime(2024, 3, 22, 12, 0).replace(tzinfo=timezone.utc),
            type=RecordType.IN,
            user=self.user,
        )
        record6 = RecordFactory(
            ref_datetime=datetime(2024, 3, 22, 17, 30).replace(tzinfo=timezone.utc),
            type=RecordType.OUT,
            user=self.user,
        )

        return [record1, record2, record3, record4, record5, record6]

    def __get_records_with_gaps(self) -> list[Record]:
        record1 = RecordFactory(
            ref_datetime=datetime(2024, 3, 21, 9, 0).replace(tzinfo=timezone.utc),
            type=RecordType.IN,
            user=self.user,
        )
        record2 = RecordFactory(
            ref_datetime=datetime(2024, 3, 21, 12, 0).replace(tzinfo=timezone.utc),
            type=RecordType.OUT,
            user=self.user,
        )
        record3 = RecordFactory(
            ref_datetime=datetime(2024, 3, 21, 13, 30).replace(tzinfo=timezone.utc),
            type=RecordType.IN,
            user=self.user,
        )

        record5 = RecordFactory(
            ref_datetime=datetime(2024, 3, 22, 12, 0).replace(tzinfo=timezone.utc),
            type=RecordType.IN,
            user=self.user,
        )

        return [record1, record2, record3, record5]
