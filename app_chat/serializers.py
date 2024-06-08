from rest_framework import serializers
from app_chat.models import Room, Message

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name','slug','user1','user2','is_deleted_user1','is_deleted_user2']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['room','user','content','date_added','is_deleted']