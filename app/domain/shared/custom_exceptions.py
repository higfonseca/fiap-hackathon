class NotFoundException(Exception):
    def __init__(self, description: str) -> None:
        super().__init__(description)


class DomainException(Exception):
    def __init__(self, description: str) -> None:
        super().__init__(description)


class InfraException(Exception):
    def __init__(self, description: str) -> None:
        super().__init__(description)


class DuplicatedException(DomainException):
    pass
