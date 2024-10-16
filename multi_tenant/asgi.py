"""
ASGI config for multi_tenant project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import notifications.routing 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multi_tenant.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP protocol for standard Django views
    "websocket": AuthMiddlewareStack(  # WebSocket protocol for WebSockets
        URLRouter(
            notifications.routing.websocket_urlpatterns  # WebSocket routes
        )
    ),
})