import json
import jwt
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("notifications", self.channel_name)


    async def disconnect(self, event):
        pass


    async def send_notification(self, event):
        message = event["message"]
        await self.send(
            text_data=json.dumps(
                {
                    "message": message
                }, ensure_ascii=False
            )
        )