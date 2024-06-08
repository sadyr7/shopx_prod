from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async

import json
from jwt import decode, InvalidTokenError
from django.conf import settings
from asgiref.sync import sync_to_async

from .models import Room, Message
from app_user.models import User

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
        

        # Подключение к комнате
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f"Подключение+ к комнате {self.room_name}")


 





#=== Комната ==========================================================================================================


    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)

        if 'message' in data:
            message = data['message']
            sender_username = data['sender_username']
            recipient_username = data['recipient_username']
            # room_slug = f"{sender_username}_{recipient_username}"

            room = await self.get_room_by_slug(self.room_name,recipient_username, sender_username)
            print(f"recieve Room: {room}")
            await self.send_message(room, message, sender_username)
        elif 'delete_room_name' in data:  # Проверяем наличие идентификатора комнаты
            sender_username = data['sender_username']
            room = data['delete_room_name']
            await self.delete_room(room,sender_username)
        else:
            print("Не удалось найти ключ 'message' или 'message_id' в JSON-объекте.")
            # self.close()
        


    async def get_room_by_slug(self,room_name,sender_username, recipient_username):
        sender = await sync_to_async(User.objects.filter(username=sender_username).first)()
        recipient = await sync_to_async(User.objects.filter(username=recipient_username).first)()
        try:
            room = await database_sync_to_async(Room.objects.get)(name=room_name)
            print(f"get_room_by_slug Комната нашлась {room}")
            return room
        except Room.DoesNotExist:
            print(f"get_room_by_slug Комната не нашлась")
            try:
                new_room = await database_sync_to_async(Room.objects.create)(name=room_name, slug=room_name,user1=sender,user2=recipient)
                await database_sync_to_async(new_room.save)()

                new_room.user1 = sender
                new_room.user2 = recipient
                print(f"get_room_by_slug Создание комнаты {new_room}")
                return new_room
            except Exception as e:
                print(f"get_room_by_slug Ошибка при создании комнаты: {e}")
                self.close()
                
            
# ============= Сообщения ================================================================
                
    async def get_last_30_messages(self):
        room_name = self.scope['url_route']['kwargs']['room_name']
        try:
            # Получаем последние 30 сообщений для указанной комнаты
            messages = Message.objects.filter(room__name=room_name).order_by('-date_added')[:2]
            return messages
        except Message.DoesNotExist:
            return []

    #Отправка сообщений
    async def send_message(self, room_name, message, sender_username):
        channel_layer = get_channel_layer()
        if room_name:
            # Формируем имя группы
            print(f'Send message: Комната нашлась ')
            group_name = f"room_{room_name}"
            await self.save_message(sender_username, room_name, message)
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

    # Чат
    async def chat_message(self, event):
        # Получаем данные из события
        message = event['message']
        username = event['username']

        # Отправляем сообщение обратно клиенту
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    #Сохранение сообщений
    async def save_message(self, username, room, message):
        try:
            user = await sync_to_async(User.objects.get)(username=username)
            room = await sync_to_async(Room.objects.get)(slug=room)
            await sync_to_async(Message.objects.create)(user=user, room=room, content=message)
            print(f"Сохраняем сообщение")
        except Exception as e:
            print(f"Error saving message: {e}")


    # Удаление сообщений
    async def delete_room(self, room_name,sender_username):
        try:
            
            room = await sync_to_async(Room.objects.get)(name=room_name)
            sender = await sync_to_async(User.objects.get)(username=sender_username)
            # Устанавливаем флаг is_deleted только для текущего пользователя
            if sender.id == room.user2_id:
                room.is_deleted_user2 = True
                await sync_to_async(room.save)()
                print(f"Флажок is_deleted_user1 установлен в True для комнаты {room} пользователем {sender}")
            elif sender.id == room.user1_id:
                room.is_deleted_user1 = True
                await sync_to_async(room.save)()
                print(f"Флажок is_deleted_user2 установлен в True для комнаты {room} пользователем {sender}")
            else:
                print("Пользователь не имеет права устанавливать флаги is_deleted.")
            if room.is_deleted_user1 and room.is_deleted_user2:
                await sync_to_async(room.delete)()
                print(f"Комната {room} удалена, так как оба пользователя установили флаги is_deleted.")

        except Room.DoesNotExist:
            # await self.send(text_data=json.dumps({'error': 'Message not found'}))
            print('Error')

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
                user = await sync_to_async(User.objects.get)(id=user_id)
                print(f"В комнату зашел пользователь {user}")
                return user
        except InvalidTokenError as e:
            print(f"Ошибка при декодировании токена: {e}")
        await self.close() 
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





