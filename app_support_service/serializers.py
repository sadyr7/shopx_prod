from rest_framework import serializers
from .models import SupportServiceRoom, SupportServiceMessage


class SupportRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportServiceRoom
        fields = ['name','slug','admin','sender','created_at',]


class SupportMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportServiceMessage
        fields = ['support_room','user','content','date_added',]