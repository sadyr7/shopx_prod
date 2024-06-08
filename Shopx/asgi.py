import os
import django
from django.core.asgi import get_asgi_application

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Shopx.settings')

# Initialize Django
django.setup()

# Get the ASGI application
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from app_chat.consumers import ChatConsumer
from app_support_service.consumers import SupportChatConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/<str:room_name>/', ChatConsumer.as_asgi()),
            path('ws/support/<str:room_name>/', SupportChatConsumer.as_asgi()),
        ])
    ),

})