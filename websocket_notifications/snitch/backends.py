from snitch.backends import AbstractBackend
from snitch.settings import ENABLED_SEND_NOTIFICATIONS

from websocket_notifications.helpers import send_to_user


class WebSocketNotificationBackend(AbstractBackend):
    """A backend class to send websocket notifications."""

    def payload(self):
        """Creates the payload of the message."""
        return {
            "notification": self.notification.id if self.notification else None,
            "event": {
                "actor_content_type": str(self.event.actor_content_type),
                "actor_object_id": self.event.actor_object_id,
                "verb": self.event.verb,
                "trigger_content_type": str(self.event.trigger_content_type),
                "trigger_object_id": self.event.trigger_object_id,
                "target_content_type": str(self.event.target_content_type),
                "target_object_id": self.event.target_object_id,
            },
        }

    def send(self):
        """Send message."""
        if ENABLED_SEND_NOTIFICATIONS:
            send_to_user(self.user, self.payload())
