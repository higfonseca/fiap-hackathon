from datetime import datetime, timezone
from unittest import IsolatedAsyncioTestCase

from freezegun import freeze_time

from app.domain.record.record_type import RecordType
from app.infrastructure.container import ApplicationContainer
from tests.factories.domain_factories import RecordFactory, UserFactory


class TestRecordPostgresRepository(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.record = RecordFactory()
        self.repository = ApplicationContainer.record_repository()

    async def test_save_WHEN_called_THEN_persists_informed_record(self):
        await self.repository.save(self.record)
        result = await self.repository.list_by_user(self.record.user.id)
        self.assertCountEqual([self.record], result)

    async def test_list_by_user_WHEN_called_RETURNS_related_records(self):
        record2 = RecordFactory(user=self.record.user)
        record_from_other_user = RecordFactory()

        await self.repository.save(self.record)
        await self.repository.save(record2)
        await self.repository.save(record_from_other_user)

        result = await self.repository.list_by_user(self.record.user.id)
        self.assertCountEqual([self.record, record2], result)

    async def test_list_by_month_and_year_WHEN_called_RETURNS_related_records(self):
        ref_month = 8
        ref_year = 2023
        ref_datetime = datetime(2023, 8, 1, 10)

        ref_user = UserFactory()
        record = RecordFactory(
            type=RecordType.IN,
            user=ref_user,
            ref_month=ref_month,
            ref_year=ref_year,
            ref_datetime=ref_datetime,
        )
        record2 = RecordFactory(
            type=RecordType.OUT,
            user=ref_user,
            ref_month=ref_month,
            ref_year=ref_year,
            ref_datetime=ref_datetime,
        )
        record3 = RecordFactory(type=RecordType.OUT, user=ref_user, ref_month=ref_month, ref_year=2024)
        record_from_other_user = RecordFactory()

        await self.repository.save(record)
        await self.repository.save(record2)
        await self.repository.save(record3)
        await self.repository.save(record_from_other_user)

        result = await self.repository.list_by_user_month_and_year(
            user_id=ref_user.id,
            ref_month=ref_month,
            ref_year=ref_year,
        )

        self.assertCountEqual([record, record2], result)

    @freeze_time("2024-03-23 19:00:00")
    async def test_get_user_todays_last_record_WHEN_called_RETURNS_user_most_recent_record(self):
        earlier_today = datetime(2024, 3, 23, 10)
        now_utc = datetime.now(timezone.utc)
        user = UserFactory()
        record = RecordFactory(user=user, ref_datetime=datetime(2020, 1, 1))
        record2 = RecordFactory(user=user, ref_datetime=earlier_today)
        record3 = RecordFactory(user=user, ref_datetime=now_utc)
        await self.repository.save(record)
        await self.repository.save(record2)
        await self.repository.save(record3)

        result = await self.repository.get_user_todays_last_record(user.id)

        self.assertEqual(record3, result)

    @freeze_time("2024-03-23 19:00:00")
    async def test_get_user_todays_last_record_WHEN_no_record_today_RETURNS_None(self):
        user = UserFactory()
        record = RecordFactory(user=user, ref_datetime=datetime(2020, 1, 1))
        record2 = RecordFactory(user=user, ref_datetime=datetime(2024, 1, 1))
        await self.repository.save(record)
        await self.repository.save(record2)

        result = await self.repository.get_user_todays_last_record(user.id)

        self.assertIsNone(result)
