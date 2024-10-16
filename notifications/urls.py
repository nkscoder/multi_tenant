from django.urls import path
from .views import *


urlpatterns = [
    path('api/rooms/', room_list_create, name='room-list-create'),
]
