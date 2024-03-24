from datetime import timezone, datetime, date, time
from unittest import IsolatedAsyncioTestCase

from app.application.use_cases.record.dtos.get_records_output import GetRecordsOutput, GetRecordsSummaryOutput, \
    GetRecordsTimesOutput
from app.domain.record.enums import RecordType
from app.infrastructure.container import ApplicationContainer
from tests.factories.domain_factories import RecordFactory, UserFactory


class TestGetRecords(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.now_utc = datetime.now(timezone.utc)
        self.user = UserFactory()

        self.record_repository = ApplicationContainer.record_repository()
        self.use_case = ApplicationContainer.get_records()

    async def test_call_WHEN_called_RETURNS_full_report_for_the_selected_month_and_year(self):
        await self.__seed()
        ref_month = 3
        ref_year = 2024

        result = await self.use_case(user_id=self.user.id, ref_month=ref_month, ref_year=ref_year)

        expected_result = GetRecordsOutput(
            records=[
                GetRecordsSummaryOutput(
                    date=date(2024, 3, 21),
                    worked_time=time(7, 30),
                    times=[
                        GetRecordsTimesOutput(
                            clock_in=time(9, 0),
                            clock_out=time(12, 0),
                        ),
                        GetRecordsTimesOutput(
                            clock_in=time(13, 30),
                            clock_out=time(18, 0),
                        ),
                    ],
                ),
                GetRecordsSummaryOutput(
                    date=date(2024, 3, 22),
                    worked_time=time(5, 30),
                    times=[
                        GetRecordsTimesOutput(
                            clock_in=time(12, 0),
                            clock_out=time(17, 30),
                        ),
                    ],
                )
            ],
            ref_month=ref_month,
            ref_year=ref_year,
        )
        self.assertCountEqual(expected_result, result)

    async def __seed(self) -> None:
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

        await self.record_repository.save(record1)
        await self.record_repository.save(record2)
        await self.record_repository.save(record3)
        await self.record_repository.save(record4)
        await self.record_repository.save(record5)
        await self.record_repository.save(record6)
