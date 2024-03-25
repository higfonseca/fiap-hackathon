# mypy: disable-error-code="misc"
import logging
from typing import Any

from app.domain.shared.message_code import MessageCode
from app.domain.shared.notification_provider_abstract import NotificationProviderAbstract


class NotificationProvider(NotificationProviderAbstract):
    def send_email(self, email: str, message_code: MessageCode, properties: dict[str, Any]) -> None:
        logging.info("Sending email notification")
        self.__send_to_provider(email, message_code, properties)

    @staticmethod
    def __send_to_provider(email: str, message_code: MessageCode, properties: dict[str, Any]) -> None:
        logging.info("Notification sent. Email: %s. Code: %s. Properties: %s", email, message_code, properties)
