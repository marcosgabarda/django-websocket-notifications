from typing import Dict

from asgiref.sync import async_to_sync
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from websocket_notifications.helpers import generate_random_code
from websocket_notifications.managers import NotificationGroupQuerySet
from websocket_notifications.settings import MESSAGE_TYPE


class NotificationGroup(TimeStampedModel):
    """This model is used to save an unique code for each object to use to
    connect for listening notifications.
    """

    code = models.CharField(_("code"), max_length=256, unique=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    objects = NotificationGroupQuerySet.as_manager()

    class Meta:
        verbose_name = _("notification group")
        verbose_name_plural = _("notification groups")
        ordering = ["-created"]

    def send(self, payload: Dict) -> None:
        """Sends the payload to the user or device."""
        from channels.layers import get_channel_layer

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            self.code, {"type": MESSAGE_TYPE, "payload": payload}
        )

    def clean(self) -> None:
        # Generates the code if it doesn't exists
        if not self.code:
            self.code = generate_random_code(self.object_id)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
