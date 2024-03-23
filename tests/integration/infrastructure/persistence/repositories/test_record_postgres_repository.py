from datetime import datetime
from unittest import IsolatedAsyncioTestCase

from app.domain.record.record_type import RecordType
from app.infrastructure.container import ApplicationContainer
from tests.factories.domain_factories import RecordFactory, UserFactory


class TestRecordPostgresRepository(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.record = RecordFactory()
        self.database_session = ApplicationContainer.session_provider()
        self.user_repository = ApplicationContainer.record_repository()
        self.record_repository = ApplicationContainer.record_repository()

    async def test_save_WHEN_called_THEN_persists_informed_record(self):
        await self.record_repository.save(self.record)
        result = await self.record_repository.list_by_user(self.record.user.id)
        self.assertCountEqual([self.record], result)

    async def test_list_by_user_WHEN_called_RETURNS_related_records(self):
        record2 = RecordFactory(user=self.record.user)
        record_from_other_user = RecordFactory()

        await self.record_repository.save(self.record)
        await self.record_repository.save(record2)
        await self.record_repository.save(record_from_other_user)

        result = await self.record_repository.list_by_user(self.record.user.id)
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

        await self.record_repository.save(record)
        await self.record_repository.save(record2)
        await self.record_repository.save(record3)
        await self.record_repository.save(record_from_other_user)

        result = await self.record_repository.list_by_month_and_year(
            user_id=ref_user.id,
            ref_month=ref_month,
            ref_year=ref_year,
        )
        
        self.assertCountEqual([record, record2], result)
