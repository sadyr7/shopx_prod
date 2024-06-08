from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import json
from jwt import decode, InvalidTokenError
from django.conf import settings
from django.db.models import Q
from channels.db import database_sync_to_async
from user_profiles.models import CustomUser
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):

#=== Вход ====================================================================================
    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name

        


        #======Проведение аутентификации пользователя============================
        headers = dict(self.scope['headers'])
        token = headers.get(b'authorization', b'').decode('utf-8').split(' ')[-1]
        if not token:
            await self.close()

        user = await self.authenticate_user(token)
        if not user:
            await self.close()
            return
        

        # Проверка наличия комнаты

        
        # await self.get_room_by_slug(self.room_name,sender_username, recipient_username)
        


        # Подключение к комнате
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f"Подключение+ к комнате {self.room_name}")


 








    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        message = data['message']
        sender_username = data['sender_username']
        recipient_username = data['recipient_username']
        # room_slug = f"{sender_username}_{recipient_username}"

        room = await self.get_room_by_slug(self.room_name,recipient_username, sender_username)
        print(f"recieve Room: {room}")
        await self.send_message(room, message, sender_username)
        


    async def get_room_by_slug(self,room_name,sender_username, recipient_username):
        sender = await sync_to_async(CustomUser.objects.get)(username=sender_username)
        recipient = await sync_to_async(CustomUser.objects.get)(username=recipient_username)
        try:
            room = await database_sync_to_async(Room.objects.get)(name=room_name)
            print(f"get_room_by_slug Комната нашлась {room}")
            return room
        except Room.DoesNotExist:
            print(f"get_room_by_slug Комната не нашлась")
            try:
                new_room = await database_sync_to_async(Room.objects.create)(name=room_name, slug=room_name)
                await database_sync_to_async(new_room.save)()

                await sync_to_async(new_room.users.add)(sender, recipient)
                print(f"get_room_by_slug Создание комнаты {new_room}")
                return new_room
            except Exception as e:
                print(f"get_room_by_slug Ошибка при создании комнаты: {e}")
                self.close()
                
            


    async def send_message(self, room_name, message, sender_username):
        channel_layer = get_channel_layer()
        if room_name:
            # Формируем имя группы
            print(f'Send message: Комната нашлась ')
            group_name = f"room_{room_name}"
            # Отправляем сообщение в группу
            await channel_layer.group_send(
                group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': sender_username
                }
            )
        else:
            print("Комната не найдена или не создана.")


    async def chat_message(self, event):
        # Получаем данные из события
        message = event['message']
        username = event['username']

        # Отправляем сообщение обратно клиенту
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    # async def save_message(self, room, sender_username, message):
    #     pass
# await self.send(text_data=json.dumps({'status': 'error', 'message': 'Authentication failed'}))

#=========== Авторизация ==============================================
    def get_token(self):
        headers = dict(self.scope['headers'])
        authorization_header = headers.get(b'authorization', b'')
        if authorization_header:
            token = authorization_header.decode('utf-8').split(' ')[-1]
            return token
        return None

    async def authenticate_user(self, token):
        try:
            decoded_token = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token.get('user_id')
            if user_id:
                user = await sync_to_async(CustomUser.objects.get)(id=user_id)
                print(f"В комнату зашел пользователь {user}")
                return user
        except InvalidTokenError:
            pass
        return None
    

#======= Выход =========================================================
    
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





