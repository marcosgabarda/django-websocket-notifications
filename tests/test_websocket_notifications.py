from test_plus import APITestCase
from test_plus.test import APITestCase, TestCase

from tests.factories import UserFactory
from websocket_notifications.models import NotificationGroup


class NotificationGroupAPITest(APITestCase):
    user_factory = UserFactory

    def setUp(self):
        self.user = self.make_user()

    def test_create_notification_group(self):
        self.assertEqual(0, NotificationGroup.objects.filter(user=self.user).count())
        with self.login(self.user):
            self.post("api_v1:notificationgroup-list")
        self.response_201()
        data = self.last_response.json()
        self.assertIn("code", data)
        self.assertEqual(1, NotificationGroup.objects.filter(user=self.user).count())

    def test_create_notification_group_already_existing(self):
        NotificationGroup.objects.get_or_create_for_user(user=self.user)
        self.assertEqual(1, NotificationGroup.objects.filter(user=self.user).count())
        with self.login(self.user):
            self.post("api_v1:notificationgroup-list")
        self.response_201()
        data = self.last_response.json()
        self.assertIn("code", data)
        self.assertEqual(1, NotificationGroup.objects.filter(user=self.user).count())


class ListenerTest(TestCase):
    user_factory = UserFactory

    def setUp(self):
        self.user = self.make_user()

    def test_get_listener_view(self):
        with self.login(self.user):
            self.get("websocket_notifications:listener")
        self.response_200()
