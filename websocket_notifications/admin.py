from django.contrib import admin

from websocket_notifications.models import NotificationGroup


@admin.register(NotificationGroup)
class NotificationGroupAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "code", "created"]
    search_fields = ["code", "user__email"]
