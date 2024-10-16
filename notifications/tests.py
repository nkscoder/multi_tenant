import json
import pytest
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.test import TestCase
from asgiref.testing import ApplicationCommunicator
from .consumers import NotificationConsumer
from .routing import application

@pytest.mark.asyncio
class NotificationConsumerTestCase(TestCase):

    async def test_websocket_connect(self):
        communicator = WebsocketCommunicator(application, "/ws/notifications/")
        connected, subprotocol = await communicator.connect()
        assert connected  # Connection should succeed

        # Disconnect
        await communicator.disconnect()

    async def test_send_and_receive_message(self):
        communicator = WebsocketCommunicator(application, "/ws/notifications/")
        connected, subprotocol = await communicator.connect()
        assert connected

        # Send message to WebSocket
        message = json.dumps({"message": "Test Notification"})
        await communicator.send_json_to({"message": "Test Notification"})

        # Receive message from WebSocket
        response = await communicator.receive_json_from()
        assert response == {"message": "Test Notification"}

        # Disconnect
        await communicator.disconnect()

    async def test_invalid_message_format(self):
        communicator = WebsocketCommunicator(application, "/ws/notifications/")
        connected, subprotocol = await communicator.connect()
        assert connected

        # Send invalid message
        await communicator.send_json_to(["Invalid message format"])

        # Receive error message
        response = await communicator.receive_json_from()
        assert response == {"error": "Invalid message format"}

        # Disconnect
        await communicator.disconnect()
