from django.urls import re_path

from websocket_notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r"ws/notifications/(?P<code>.+)/$", NotificationConsumer)
]
