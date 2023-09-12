from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WebsocketNotificationsAppConfig(AppConfig):
    name = "websocket_notifications"
    verbose_name = _("Websocket notifications")
    default_auto_field = "django.db.models.BigAutoField"
