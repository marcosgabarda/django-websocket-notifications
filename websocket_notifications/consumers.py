import json
from typing import Dict

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from websocket_notifications.models import NotificationGroup


class NotificationConsumer(AsyncWebsocketConsumer):
    """Consumer for sending notification to the client."""

    @database_sync_to_async
    def get_notification_group(self, code: str):
        return NotificationGroup.objects.filter(code=code).first()

    async def connect(self):
        """When a consumer is connected, we get the code from the URL, to join to
        the group."""
        self.code = self.scope["url_route"]["kwargs"]["code"]
        if await self.get_notification_group(self.code):
            await self.channel_layer.group_add(self.code, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        """On disconnect, exit from the group."""
        await self.channel_layer.group_discard(self.code, self.channel_name)

    async def notification_message(self, event: Dict):
        """When received a message from a notification."""
        payload = event["payload"]
        await self.send(text_data=json.dumps({"payload": payload}))
