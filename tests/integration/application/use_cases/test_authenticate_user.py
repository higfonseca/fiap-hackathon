from unittest import IsolatedAsyncioTestCase

from app.domain.shared.custom_exceptions import NotAuthenticatedException
from app.infrastructure.container import ApplicationContainer
from app.application.use_cases.user.authenticate_user import AuthenticateUser
from app.shared.services.jwt_token_service import JwtTokenService
from tests.factories.domain_factories import UserFactory

from freezegun import freeze_time


class TestAuthenticateUser(IsolatedAsyncioTestCase):
    def setUp(self):
        self.user_repository = ApplicationContainer.user_repository()
        self.use_case = ApplicationContainer.authenticate_user()
        self.authenticate_user = AuthenticateUser(
            user_repository=self.user_repository,
        )
        self.user_password = "fake-password"
        self.user = UserFactory(password=self.user_password)
        self.jwt_token_service = JwtTokenService()

    @freeze_time("2024-03-22")
    async def test_call_WHEN_valid_user_using_email_RETURNS_token(self):
        await self.user_repository.save(self.user)
        expected_token = self.jwt_token_service.generate_access_token(self.user)

        token = await self.authenticate_user(self.user.work_email, self.user_password)

        self.assertEqual(expected_token, token)

    @freeze_time("2024-03-22")
    async def test_call_WHEN_valid_user_using_enrollment_RETURNS_token(self):
        await self.user_repository.save(self.user)
        expected_token = self.jwt_token_service.generate_access_token(self.user)

        token = await self.authenticate_user(self.user.enrollment, self.user_password)

        self.assertEqual(expected_token, token)

    async def test_call_WHEN_wrong_password_THEN_raises_not_authenticated_exception(self):
        await self.user_repository.save(self.user)
        with self.assertRaises(NotAuthenticatedException):
            await self.authenticate_user(self.user.work_email, "wrong_password")

    async def test_authenticate_user_failed_user_not_found(self):
        with self.assertRaises(NotAuthenticatedException):
            await self.authenticate_user("nonexistent@fake.com", "any_password")
