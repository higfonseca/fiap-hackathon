from app.domain.shared.optional_enum import OptionalEnum


class MessageCode(str, OptionalEnum):
    MONTH_REPORT = "MONTH_REPORT"
