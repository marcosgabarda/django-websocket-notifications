from typing import TYPE_CHECKING, Dict, Tuple

from django.db import models

if TYPE_CHECKING:
    from websocket_notifications.models import NotificationGroup


class NotificationGroupQuerySet(models.QuerySet):
    def get_or_create_for_user(self, user) -> Tuple["NotificationGroup", bool]:
        """Abstraction for create a notification channel from a given user."""
        if self.filter(user=user).exists():
            return self.filter(user=user).first(), False
        instance = self.model(user=user)
        instance.save()
        return instance, True

    def send(self, payload: Dict) -> None:
        """Sends to a queryset of notification channels."""
        for instance in self.iterator():
            instance.send(payload)
