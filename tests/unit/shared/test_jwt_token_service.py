from datetime import datetime, timedelta, timezone
from unittest import TestCase
from jose import JWTError, jwt
from freezegun import freeze_time

from app.infrastructure.settings import settings

from app.shared.services.jwt_token_service import JwtTokenService
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

    @freeze_time("2024-03-23")
    def test_decode_WHEN_called_with_valid_token_RETURNS_payload(self):
        token = self.jwt_token_service.generate_access_token(self.mock_user)

        decoded_payload = self.jwt_token_service.decode(token.access_token)

        self.assertEqual(decoded_payload["sub"], str(self.mock_user.id))

    def test_decode_WHEN_called_with_invalid_signature_THROWS_exception(self):
        with self.assertRaises(JWTError):
            invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiZXhwIjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

            self.jwt_token_service.decode(invalid_token)

    @freeze_time("2024-03-23")
    def test_decode_WHEN_called_with_expired_token_THROWS_exception(self):
        token = self.jwt_token_service.generate_access_token(self.mock_user)

        with self.assertRaises(JWTError):
            with freeze_time("2024-03-24"):
                self.jwt_token_service.decode(token.access_token)
