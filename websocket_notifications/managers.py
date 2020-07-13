from django.db import models


class NotificationGroupQuerySet(models.QuerySet):
    def get_or_create_for_user(self, user):
        """Abstraction for create a notification channel from a given user."""
        if self.filter(user=user).exists():
            return self.filter(user=user).first(), False
        instance = self.model(user=user)
        instance.save()
        return instance, True

    def send(self, payload):
        """Sends to a queryset of notification channels."""
        for instance in self.iterator():
            instance.send(payload)
