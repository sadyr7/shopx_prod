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
        print(f"Подключение к комнате {self.room_name} пользователем {self.scope['user']}")

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
        recipient_username = data.get('recipient_username')

        if recipient_username:
            # Отправить сообщение обоим участникам комнаты
            await self.send_message_to_users(sender_username, recipient_username, message)
        else:
            # Обработать случай, когда recipient_username отсутствует в сообщении
            print("Получатель не указан")

    async def send_message_to_users(self, sender_username, recipient_username, message):
        room_sender = await self.get_or_create_room(sender_username, recipient_username)
        await self.save_message(sender_username, room_sender.slug, message)

        # Отправляем сообщение в групповой канал, связанный с комнатой отправителя
        await self.channel_layer.group_send(
            room_sender.slug,
            {
                'type': 'chat_message',
                'message': message,
                'username': sender_username
            }
        )

        room_recipient = await self.get_or_create_room(recipient_username, sender_username)
        await self.save_message(sender_username, room_recipient.slug, message)

        # Отправляем сообщение в групповой канал, связанный с комнатой получателя
        await self.channel_layer.group_send(
            room_recipient.slug,
            {
                'type': 'chat_message',
                'message': message,
                'username': sender_username
            }
        )

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
        recipient = await sync_to_async(CustomUser.objects.get)(username=recipient_username)

        existing_room = await sync_to_async(Room.objects.filter(users=sender).filter(users=recipient).first)()
        if existing_room:
            return existing_room

        room_name = f"{sender_username}_{recipient_username}"
        room_slug = f"{sender_username}_{recipient_username}"
        try:
            new_room = await sync_to_async(Room.objects.create)(name=room_name, slug=room_slug)
            await sync_to_async(new_room.users.add)(sender, recipient)
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
