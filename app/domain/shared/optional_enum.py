from __future__ import annotations

from enum import Enum
from typing import Optional


class OptionalEnum(Enum):
    @classmethod
    def get(cls, item: str) -> Optional[OptionalEnum]:
        try:
            return cls(item.upper())
        except Exception:
            return None
