from datetime import datetime, timedelta, timezone
from unittest import IsolatedAsyncioTestCase


from app.domain.record.record_type import RecordType
from app.infrastructure.container import ApplicationContainer
from tests.factories.domain_factories import UserFactory, RecordFactory


class TestCreateRecord(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.now_utc = datetime.now(timezone.utc)
        self.user = UserFactory()

        self.user_repository = ApplicationContainer.user_repository()
        self.record_repository = ApplicationContainer.record_repository()
        self.use_case = ApplicationContainer.create_record()

    async def test_call_WHEN_user_never_clocked_in_THEN_saves_new_record_with_type_clock_in(self):
        await self.user_repository.save(self.user)
        await self.use_case(user_id=self.user.id)

        persisted_record = await self.record_repository.get_user_todays_last_record(user_id=self.user.id)

        self.assertEqual(self.user, persisted_record.user)
        self.assertEqual(RecordType.IN, persisted_record.type)

    async def test_call_WHEN_user_already_clocked_in_THEN_saves_new_record_with_type_clock_out(self):
        record = RecordFactory(user=self.user, ref_datetime=self.now_utc - timedelta(seconds=10), type=RecordType.IN)
        await self.record_repository.save(record)

        await self.user_repository.save(self.user)
        await self.use_case(user_id=self.user.id)

        persisted_record = await self.record_repository.get_user_todays_last_record(user_id=self.user.id)

        self.assertEqual(self.user, persisted_record.user)
        self.assertEqual(RecordType.OUT, persisted_record.type)
