from rest_framework import generics, permissions
from rest_framework.response import Response

from django.http import Http404

from .serializers import SupportRoomSerializer, SupportMessageSerializer

from .models import SupportServiceRoom, SupportServiceMessage

class SupportRoomRetrieveAPIView(generics.RetrieveAPIView):
    queryset = SupportServiceRoom.objects.all()
    serializer_class = SupportRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user
        # Получить все комнаты, в которых текущий пользователь является создателем
        created_rooms = SupportServiceRoom.objects.filter(admin=user)
        # Получить все комнаты, в которых текущий пользователь участвует
        joined_rooms = SupportServiceRoom.objects.filter(sender=user)
        # Объединить списки созданных и присоединенных комнат
        queryset = created_rooms | joined_rooms
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def get(self, request, *args, **kwargs):
        room = self.get_object()
        messages = SupportServiceMessage.objects.filter(support_room=room)[:25]
        serializer = self.get_serializer(room)
        data = serializer.data
        data['messages'] = SupportMessageSerializer(messages, many=True).data
        return Response(data)



class SupportRoomCreateAPIView(generics.CreateAPIView):
    queryset = SupportServiceRoom.objects.all()
    serializer_class = SupportRoomSerializer
    permission_classes = [permissions.IsAuthenticated]



class SupportRoomDeleteAPIView(generics.DestroyAPIView):
    queryset = SupportServiceRoom.objects.all()
    serializer_class = SupportRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user
        # Получить только те комнаты, которые администрирует текущий пользователь
        queryset = SupportServiceRoom.objects.filter(admin=user)
        return queryset

    

    



class SupportRoomListAPIView(generics.ListAPIView):
    # queryset = Room.objects.all()
    serializer_class = SupportRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Получить все комнаты, в которых текущий пользователь является создателем
        created_rooms = SupportServiceRoom.objects.filter(admin=user)
        # Получить все комнаты, в которых текущий пользователь участвует
        joined_rooms = SupportServiceRoom.objects.filter(sender=user)
        # Объединить списки созданных и присоединенных комнат и убрать дубликаты
        queryset = created_rooms.union(joined_rooms)
        return queryset