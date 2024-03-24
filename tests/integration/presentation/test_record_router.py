from unittest import IsolatedAsyncioTestCase

from starlette import status

from app.domain.record.record_type import RecordType
from app.infrastructure.container import ApplicationContainer
from tests.factories.domain_factories import UserFactory
from tests.helpers.auth_token_helper import AuthTokenHelper


class TestRecordRouter(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.base_route = "/records"
        self.user = UserFactory()

        self.user_repository = ApplicationContainer.user_repository()
        self.record_repository = ApplicationContainer.record_repository()

    async def test_post_WHEN_called_RETURNS_201(self):
        await self.user_repository.save(self.user)
        auth_header = AuthTokenHelper.get_valid_token_headers(self.user)

        response = self.client.post(url=f"{self.base_route}", headers=auth_header)

        persisted_record = await self.record_repository.get_user_todays_last_record(user_id=self.user.id)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user, persisted_record.user)
        self.assertEqual(RecordType.IN, persisted_record.type)

    async def test_post_WHEN_user_not_exists_RETURNS_404(self):
        auth_header = AuthTokenHelper.get_valid_token_headers(self.user)

        response = self.client.post(url=f"{self.base_route}", headers=auth_header)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    async def test_post_WHEN_user_not_authenticated_RETURNS_401(self):
        response = self.client.post(url=f"{self.base_route}", headers=AuthTokenHelper.get_invalid_token_headers())

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
