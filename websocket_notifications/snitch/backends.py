from typing import TYPE_CHECKING, Dict

from snitch.backends import AbstractBackend
from snitch.settings import ENABLED_SEND_NOTIFICATIONS

from websocket_notifications.helpers import send_to_user

if TYPE_CHECKING:
    from django.contrib.contenttypes.models import ContentType


class WebSocketNotificationBackend(AbstractBackend):
    """A backend class to send websocket notifications."""

    @staticmethod
    def _content_type_serializer(content_type: "ContentType"):
        if content_type:
            return f"{content_type.app_label}.{content_type.model}"

    def payload(self) -> Dict:
        """Creates the payload of the message."""
        return {
            "notification": self.notification.id if self.notification else None,
            "event": {
                "actor_content_type": self._content_type_serializer(
                    self.event.actor_content_type
                ),
                "actor_object_id": self.event.actor_object_id,
                "verb": self.event.verb,
                "trigger_content_type": self._content_type_serializer(
                    self.event.trigger_content_type
                ),
                "trigger_object_id": self.event.trigger_object_id,
                "target_content_type": self._content_type_serializer(
                    self.event.target_content_type
                ),
                "target_object_id": self.event.target_object_id,
            },
        }

    def send(self) -> None:
        """Send message."""
        if ENABLED_SEND_NOTIFICATIONS:
            send_to_user(self.user, self.payload())
