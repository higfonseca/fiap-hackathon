from dataclasses import dataclass
from uuid import UUID


@dataclass(kw_only=True, init=True)
class User:
    id: UUID
    name: str
    work_email: str
    enrollment: str
    password: str
