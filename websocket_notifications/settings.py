from django.conf import settings

# Needed to build and publish
# ------------------------------------------------------------------------------
SECRET_KEY = "websocket_notifications"

# Specific project configuration
# ------------------------------------------------------------------------------
MESSAGE_TYPE = getattr(
    settings, "WEBSOCKET_NOTIFICATIONS_MESSAGE_TYPE", "notification_message"
)
