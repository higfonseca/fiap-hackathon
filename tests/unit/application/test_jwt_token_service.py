from datetime import datetime, timedelta, timezone
from unittest import TestCase
from jose import jwt
from freezegun import freeze_time

from app.infrastructure.settings import settings

from app.application.services.jwt_token_service import JwtTokenService
from tests.factories.domain_factories import UserFactory


class TestJwtTokenService(TestCase):
    def setUp(self) -> None:
        self.jwt_token_service = JwtTokenService()
        self.secret_key = settings.jwt_token_key
        self.algorithm = "HS256"
        self.mock_user = UserFactory()

    @freeze_time("2024-03-23")
    def test_generate_access_token_expiration_WHEN_called_RETURNS_token_with_correct_data(self):
        expected_expiration = datetime.now(timezone.utc) + timedelta(
            minutes=JwtTokenService.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        token = self.jwt_token_service.generate_access_token(self.mock_user)

        decoded_token = jwt.decode(token.access_token, self.secret_key, algorithms=[self.algorithm])
        self.assertEqual(decoded_token["sub"], self.mock_user.id)
        self.assertEqual(decoded_token["exp"], expected_expiration.timestamp())
