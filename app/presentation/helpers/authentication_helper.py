from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.domain.user.user_errors import UserErrors
from app.shared.services.jwt_token_service import JwtTokenService


class AuthenticationHelper:
    @staticmethod
    def get_current_user_id(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]) -> UUID:
        not_authenticated_exception = UserErrors.not_authenticated()
        try:
            decoded_token = JwtTokenService().decode(token)  # type:ignore[arg-type]
            user_id: str | None = decoded_token.get("sub")
            if user_id is None:
                raise not_authenticated_exception
            return UUID(user_id)
        except JWTError as exc:
            raise not_authenticated_exception from exc
