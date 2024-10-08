from app.domain.shared.custom_exceptions import (
    DomainException,
    InfraException,
    NotAuthenticatedException,
    NotFoundException,
)


class UserErrors:
    @staticmethod
    def not_found() -> NotFoundException:
        return NotFoundException("User not found")

    @staticmethod
    def persist() -> InfraException:
        return InfraException("Error persisting user")

    @staticmethod
    def duplicated() -> DomainException:
        return DomainException("User already exists")

    @staticmethod
    def not_authenticated() -> NotAuthenticatedException:
        return NotAuthenticatedException("User could not be authenticated")
