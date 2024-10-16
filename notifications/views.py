from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer
# Create your views here.
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_notification(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notifications',
        {
            'type': 'send_notification',
            'message': message,
        }
    )






@api_view(['GET', 'POST'])
def room_list_create(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
