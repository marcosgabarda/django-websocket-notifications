from django.urls import path

from websocket_notifications.views import NotificationsListenerView

app_name = "websocket_notifications"
urlpatterns = [path("listener/", NotificationsListenerView.as_view(), name="listener")]
