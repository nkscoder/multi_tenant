from django.urls import re_path,path
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
    # re_path(r'ws/chat/$', PrivateChatConsumer.as_asgi()),
    path('ws/chat/<str:username>/', consumers.PrivateMessageConsumer.as_asgi()),

]

