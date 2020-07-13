from typing import Any, Sequence

import factory
from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, Faker, post_generation

from websocket_notifications.models import NotificationGroup


class UserFactory(DjangoModelFactory):

    username = Faker("user_name")
    first_name = Faker("first_name")
    last_name = Faker("last_name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = Faker(
            "password",
            length=42,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        ).generate(extra_kwargs={})
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


class NotificationGroupFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = NotificationGroup
