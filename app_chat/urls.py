from django.urls import path

from app_chat.views import *

urlpatterns = [
    path('', RoomListAPIView.as_view(), name='rooms'),
    path('create/', RoomCreateAPIView.as_view(), name='rooms-create'),
    path('delete/<slug:slug>/', RoomDeleteAPIView.as_view(), name='rooms-delete'),
    path('<slug:slug>/', RoomRetrieveAPIView.as_view(), name='room-detail'),
]