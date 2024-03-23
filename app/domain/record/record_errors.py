from app.domain.shared.custom_exceptions import DomainException, InfraException, NotFoundException


class RecordErrors:
    @staticmethod
    def not_found() -> NotFoundException:
        return NotFoundException("Record not found")

    @staticmethod
    def persist() -> InfraException:
        return InfraException("Error persisting record")

    @staticmethod
    def duplicated() -> DomainException:
        return DomainException("Record already exists")
