from dataclasses import dataclass
from enum import Enum


class ErrorType(Enum):
    domain = "domain"
    infra = "infra"
    not_found = "not_found"


@dataclass
class CustomError:
    error_type: ErrorType
    code: str
    description: str | None = None
