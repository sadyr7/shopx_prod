from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('list/vip/', VipListApiView.as_view()),
    path('detail/vip/<int:pk>/', VipDetailApiView.as_view()),
    path('create/vip/', VipCreateApiView.as_view()),
    path('rud/vip/<int:pk>/', VipRUDApiView.as_view()),
]


