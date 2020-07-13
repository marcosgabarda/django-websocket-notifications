from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from websocket_notifications.api.rest_framework import NotificationGroupViewSet

app_name = "api_v1"

router = routers.DefaultRouter()
router.register("websocket-notifications/groups", viewset=NotificationGroupViewSet)
urlpatterns = [path("", include(router.urls))]
