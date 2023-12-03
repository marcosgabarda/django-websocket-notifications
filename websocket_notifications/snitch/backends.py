from typing import TYPE_CHECKING, Dict, Optional

from snitch.settings import ENABLED_SEND_NOTIFICATIONS

from websocket_notifications.helpers import send_message

if TYPE_CHECKING:
    from django.contrib.contenttypes.models import ContentType
    from django.db import models
    from snitch.handlers import EventHandler
    from snitch.models import Event, Notification


class WebSocketNotificationBackend:
    """A backend class to send websocket notifications."""

    def __init__(
        self,
        notification: Optional["Notification"] = None,
        event: Optional["Event"] = None,
        user: Optional[models.Model] = None,
    ):
        assert notification is not None or (
            event is not None and user is not None
        ), "You should provide a notification or an event and an user."

        self.notification: Optional["Notification"] = notification
        self.event: Optional["Event"] = event
        self.user: Optional[models.Model] = user
        if self.notification:
            self.handler: "EventHandler" = self.notification.handler()
            self.user = self.notification.content_object
        elif self.event:
            self.handler = self.event.handler()

    @staticmethod
    def _content_type_serializer(content_type: Optional["ContentType"]):
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
            }
            if self.event
            else None,
        }

    def send(self) -> None:
        """Send message."""
        if ENABLED_SEND_NOTIFICATIONS:
            send_message(obj=self.user, payload=self.payload())
