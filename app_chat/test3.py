from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import json


from user_profiles.models import CustomUser
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Установка соединения WebSocket
        await self.accept()

        # Получение id комнаты из URL-адреса
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name
        print(f"Подключение+ к комнате {self.room_name}")
        # Присоединение к комнате
        #await self.join_room(self.room_name)



    async def disconnect(self, close_code):
        print("выходим disconnect")
        await self.close()
        await self.leave_room(self.room_group_name)
        print("disconnect вызван")


    async def leave_room(self, room_group_name):
        channel_layer = get_channel_layer()
        print("выходим leave_room")
        await channel_layer.group_discard(
            room_group_name,
            self.channel_name
        )
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        message = data['message']
        sender_username = data['sender_username']

        # Проверяем наличие ключа 'recipient_username' в объекте data
        if 'recipient_username' in data:
            recipient_username = data['recipient_username']
            room = await self.get_or_create_room(sender_username, recipient_username)
            await self.save_message(sender_username, room.slug, message)
            await self.channel_layer.group_send(
                room.slug,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': sender_username
                }
            )
        else:
            # Обрабатываем случай, когда recipient_username отсутствует в сообщении
            print("Получатель не указан")


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender_username  = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': sender_username
        }))


    async def get_or_create_room(self, sender_username, recipient_username):
        sender = await sync_to_async(CustomUser.objects.get)(username=sender_username)
        print("Sender:", sender)
        recipient = await sync_to_async(CustomUser.objects.get)(username=recipient_username)
        print("Recipient:", recipient)

        existing_room = await sync_to_async(Room.objects.filter(users=sender).filter(users=recipient).first)()
        if existing_room:
            return existing_room

        room_name = f"{sender_username}_{recipient_username}"
        room_slug = f"{sender_username}_{recipient_username}"
        try:
            new_room = await sync_to_async(Room.objects.create)(name=room_name, slug=room_slug)
            print("New room created:", new_room)
            await sync_to_async(new_room.users.add)(sender, recipient)
            print("Users added to room")
            return new_room
        except Exception as e:
            print(f"Error creating room: {e}")
            return None

    async def save_message(self, username, room, message):
        try:
            user = await sync_to_async(CustomUser.objects.get)(username=username)
            room = await sync_to_async(Room.objects.get)(slug=room)
            await sync_to_async(Message.objects.create)(user=user, room=room, content=message)
        except Exception as e:
            print(f"Error saving message: {e}")