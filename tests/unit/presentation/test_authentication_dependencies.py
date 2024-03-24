from unittest import TestCase

from app.domain.shared.custom_exceptions import NotAuthenticatedException
from app.presentation.dependencies.authentication_dependencies import AuthenticationDependencies

from app.shared.services.jwt_token_service import JwtTokenService
from tests.factories.domain_factories import UserFactory


class TestAuthenticationDependencies(TestCase):
    def setUp(self) -> None:
        self.jwt_token_service = JwtTokenService()
        self.user = UserFactory()

    def test_get_current_user_id_WHEN_called_with_valid_token_RETURNS_user_id(self):
        token_service = JwtTokenService()
        token = token_service.generate_access_token(self.user)

        result = AuthenticationDependencies.get_current_user_id(token=token.access_token)

        self.assertEqual(str(result), self.user.id)

    def test_get_current_user_id_WHEN_called_with_invalid_token_THEN_raises_exception(self):
        invalid_token = "some.invalid.token"

        with self.assertRaises(NotAuthenticatedException):
            AuthenticationDependencies.get_current_user_id(token=invalid_token)
