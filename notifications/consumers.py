import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer

logger = logging.getLogger(__name__)

import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class PrivateMessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.room_group_name = f'chat_{self.username}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        logger.info(f"WebSocket connected: {self.channel_name} for room {self.room_group_name}")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"WebSocket disconnected: {self.channel_name} from room {self.room_group_name}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        recipient = data.get('recipient')  # Get the recipient from the message

        logger.info(f"Message received from {self.username}: {message}")

        # Check if a recipient is provided
        if recipient:
            recipient_group_name = f'chat_{recipient}'
            
            # Send message to the recipient's room group
            await self.channel_layer.group_send(
                recipient_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': self.username
                }
            )
            logger.info(f"Sending message from {self.username} to {recipient_group_name}: {message}")
        else:
            logger.warning("No recipient specified")

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
