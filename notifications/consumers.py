import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer

logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """Handle WebSocket connection."""
        try:
            self.group_name = 'notifications'
            # Join group for notifications
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            logger.info(f"WebSocket connected: {self.channel_name}")
        except Exception as e:
            logger.error(f"Error while connecting WebSocket: {e}")
            await self.close(code=1011)  # 1011 indicates server error during WebSocket connection

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        try:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
            logger.info(f"WebSocket disconnected: {self.channel_name}")
        except Exception as e:
            logger.error(f"Error while disconnecting WebSocket: {e}")
        finally:
            raise StopConsumer()

    async def receive(self, text_data):
        """Receive and process messages from WebSocket."""
        try:
            logger.info("Message received from client.")
            text_data_json = json.loads(text_data)  # Decode incoming JSON data
            
            # Validate message format
            if not isinstance(text_data_json, dict):
                raise ValueError("Invalid message format, expected a dictionary.")

            message = text_data_json.get('message', '').strip()  # Safely retrieve and strip whitespace

            if message:
                logger.info(f"Received notification: {message}")
                # Broadcast message to the group
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'send_notification',
                        'message': message
                    }
                )
            else:
                logger.warning("Empty message received.")
                await self.send(text_data=json.dumps({
                    'error': 'Empty message received'
                }))
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            await self.send(text_data=json.dumps({
                'error': 'Invalid message format'
            }))
        except ValueError as e:
            logger.error(f"Message validation error: {e}")
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))
        except Exception as e:
            logger.error(f"Error in receive method: {e}")
            await self.close(code=1011)  # Server error during message handling

    async def send_notification(self, event):
        """Send notifications to WebSocket."""
        try:
            message = event.get('message', '').strip()
            if message:
                logger.info(f"Sending notification to client: {message}")
                # Send message to WebSocket
                await self.send(text_data=json.dumps({
                    'message': message
                }))
            else:
                logger.warning("No message to send.")
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
            await self.close(code=1011)  # Server error during notification sending
