# mypy: disable-error-code="misc"
from abc import ABC, abstractmethod
from typing import Any

from app.domain.shared.message_code import MessageCode


class NotificationProviderAbstract(ABC):
    @abstractmethod
    def send_email(self, email: str, message_code: MessageCode, properties: dict[str, Any]) -> None:
        pass
