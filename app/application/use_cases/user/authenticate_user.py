from app.application.dtos.token import Token
from app.application.services.jwt_token_service import JwtTokenService
from app.domain.shared.custom_exceptions import NotFoundException
from app.domain.user.user_errors import UserErrors
from app.domain.user.user_repository_abstract import UserRepositoryAbstract
from app.shared.password_hash_utils import PasswordHashUtils


class AuthenticateUser:
    def __init__(self, user_repository: UserRepositoryAbstract):
        self.__user_repository = user_repository

    async def __call__(self, identifier: str, password: str) -> Token:
        try:
            user = await self.__user_repository.find_by_work_email_or_enrollment(identifier)
        except NotFoundException as exc:
            raise UserErrors.not_authenticated() from exc
        is_user_authenticated = PasswordHashUtils.verify_password(password, user.password)
        if not is_user_authenticated:
            raise UserErrors.not_authenticated()

        return JwtTokenService().generate_access_token(user)
