from app.domain.user.user import User
from app.shared.services.jwt_token_service import JwtTokenService


class AuthTokenHelper:
    @staticmethod
    def get_valid_token_headers(user: User):
        auth_token = JwtTokenService().generate_access_token(user)

        return {"Authorization": f"Bearer {auth_token.access_token}"}

    @staticmethod
    def get_invalid_token_headers():
        return {"Authorization": "Bearer invalid_token"}
