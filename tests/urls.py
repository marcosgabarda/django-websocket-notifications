from django.urls import include, path


urlpatterns = [
    path(
        "websocket-notifications/",
        include("websocket_notifications.urls", namespace="websocket_notifications"),
    ),
    path("api/v1/", include("tests.router", namespace="api_v1")),
]
