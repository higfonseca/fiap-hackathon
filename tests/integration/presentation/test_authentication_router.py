from unittest import IsolatedAsyncioTestCase

from starlette import status

from app.infrastructure.container import ApplicationContainer
from tests.factories.domain_factories import UserFactory


class TestAuthenticationRouter(IsolatedAsyncioTestCase):
    def setUp(self):
        self.base_route = "/authenticate"
        self.user_repository = ApplicationContainer.user_repository()
        self.user = UserFactory()
        self.correct_password = self.user.password
        self.wrong_password = "wrong_password"

    async def test_post_WHEN_user_is_authenticated_RETURNS_token(self):
        await self.user_repository.save(self.user)

        response = self.client.post(
            self.base_route,
            data={
                "username": self.user.work_email,
                "password": self.correct_password,
            },
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("access_token", response.json())
        self.assertEqual("bearer", response.json()["token_type"])

    async def test_post_WHEN_user_with_wrong_password_RETURNS_http_401(self):
        await self.user_repository.save(self.user)

        response = self.client.post(
            self.base_route,
            data={"username": self.user.work_email, "password": self.wrong_password},
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual("User could not be authenticated", response.json()["description"])

    async def test_authenticate_WHEN_nonexistent_user_RETURNS_http_401(self):
        response = self.client.post(
            self.base_route, data={"username": "nonexistent@fake.com", "password": "any_password"}
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual("User could not be authenticated", response.json()["description"])
