from typing import TYPE_CHECKING, Dict, Tuple

from django.contrib.contenttypes.models import ContentType
from django.db import models

if TYPE_CHECKING:
    from websocket_notifications.models import NotificationGroup


class NotificationGroupQuerySet(models.QuerySet):
    def get_or_create_for_object(
        self, obj: models.Model
    ) -> Tuple["NotificationGroup", bool]:
        """Abstraction for create a notification channel from a given object."""
        content_type: ContentType = ContentType.objects.get_for_model(obj.__class__)
        object_id: int = obj.pk
        return super().get_or_create(content_type=content_type, object_id=object_id)

    def send(self, payload: Dict) -> None:
        """Sends to a queryset of notification channels."""
        for instance in self.iterator():
            instance.send(payload)
