from django.urls import path

from .views import *

urlpatterns = [
    path('', SupportRoomListAPIView.as_view(), name='support-rooms'),
    path('create/', SupportRoomCreateAPIView.as_view(), name='support-rooms-create'),
    path('delete/<slug:slug>/', SupportRoomDeleteAPIView.as_view(), name='support-rooms-delete'),
    path('<slug:slug>/', SupportRoomRetrieveAPIView.as_view(), name='support-room-detail'),
]