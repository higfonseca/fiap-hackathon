# mypy: disable-error-code="import-untyped, no-any-return"
from datetime import datetime, timedelta, timezone

from jose import jwt

from app.application.dtos.token import Token
from app.domain.user.user import User
from app.infrastructure.settings import settings


class JwtTokenService:
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def generate_access_token(self, user: User) -> Token:
        token_type = "bearer"
        token_expiration_timedelta = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_expiration_time = datetime.now(timezone.utc) + token_expiration_timedelta
        data_to_encode = {"sub": str(user.id), "exp": token_expiration_time}

        encoded_jwt = jwt.encode(data_to_encode, settings.jwt_token_key, algorithm=self.ALGORITHM)

        return Token(access_token=encoded_jwt, token_type=token_type)
