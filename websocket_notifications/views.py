from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from websocket_notifications.models import NotificationGroup


class NotificationsListenerView(LoginRequiredMixin, View):
    """Testing view for listen to notifications."""

    template_name = "websocket_notifications/listener.html"

    def get(self, request):
        """Creates the channel on the fly."""
        group, _ = NotificationGroup.objects.get_or_create_for_user(user=request.user)
        context = {"group": group}
        return render(request, self.template_name, context=context)
