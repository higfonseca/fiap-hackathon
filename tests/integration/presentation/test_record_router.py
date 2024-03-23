from datetime import datetime, timezone
from unittest import IsolatedAsyncioTestCase

from freezegun import freeze_time
from starlette import status

from app.domain.record.record_type import RecordType
from app.infrastructure.container import ApplicationContainer
from tests.factories.domain_factories import UserFactory


@freeze_time("2024-03-23 10:00:00")
class TestRecordRouter(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.base_route = "/records"
        self.user = UserFactory()
        self.now_utc = datetime.now(timezone.utc)

        self.user_repository = ApplicationContainer.user_repository()
        self.record_repository = ApplicationContainer.record_repository()

    async def test_post_WHEN_called_RETURNS_201(self):
        await self.user_repository.save(self.user)

        response = self.client.post(url=f"{self.base_route}/{self.user.id}")

        persisted_record = await self.record_repository.get_user_todays_last_record(user_id=self.user.id)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user, persisted_record.user)
        self.assertEqual(RecordType.IN, persisted_record.type)

    async def test_post_WHEN_user_not_exists_RETURNS_404(self):
        response = self.client.post(url=f"{self.base_route}/{self.user.id}")
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)