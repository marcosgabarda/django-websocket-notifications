from typing import Dict

from asgiref.sync import async_to_sync
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from websocket_notifications.helpers import generate_random_code
from websocket_notifications.managers import NotificationGroupQuerySet
from websocket_notifications.settings import MESSAGE_TYPE


class NotificationGroup(TimeStampedModel):
    """This model is used to save an unique code for each user to use to connect for
    listenign notifications.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        related_name="notification_group",
        on_delete=models.CASCADE,
    )
    code = models.CharField(_("code"), max_length=256, unique=True, blank=True)

    objects = NotificationGroupQuerySet.as_manager()

    class Meta:
        verbose_name = _("notification group")
        verbose_name_plural = _("notification groups")
        ordering = ["-created"]

    def generate_random_code(self) -> str:
        """Generates a random code using the user ID and the current time."""
        return generate_random_code(self.user.pk)

    def send(self, payload: Dict) -> None:
        """Sends the payload to the user."""
        from channels.layers import get_channel_layer

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            self.code, {"type": MESSAGE_TYPE, "payload": payload}
        )

    def clean(self) -> None:
        # Generates the code if it doesn't exists
        if not self.code:
            self.code = self.generate_random_code()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
