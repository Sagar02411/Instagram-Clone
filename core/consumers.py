import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth.models import User

# class ChatConsumer(AsyncWebsocketConsumer):
# 	async def connect(self):
# 		self.roomGroupName = "group_chat"
# 		await self.channel_layer.group_add(
# 			self.roomGroupName ,
# 			self.channel_name
# 		)

# 		await self.accept()
# 	async def disconnect(self , close_code):
# 		await self.channel_layer.group_discard(
# 			self.roomGroupName , 
# 			self.channel_layer 
# 		)
		
# 	async def receive(self, text_data):
# 		text_data_json = json.loads(text_data)
# 		message = text_data_json["message"]
# 		username = text_data_json["username"]
# 		await self.channel_layer.group_send(
# 			self.roomGroupName,{
# 				"type" : "sendMessage" ,
# 				"message" : message , 
# 				"username" : username ,
# 			})
# 	async def sendMessage(self , event) : 
# 		message = event["message"]
# 		username = event["username"]
# 		await self.send(text_data = json.dumps({"message":message ,"username":username}))


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Authenticate user
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            await self.accept()

    async def disconnect(self, close_code):
        # Clean up on disconnect
        pass

    async def receive(self, text_data):
        data_json = json.loads(text_data)
        message = data_json['message']
        receiver_id = data_json['receiver_id']
        sender = self.scope["user"]

        # Save message to database
        new_message = Message.objects.create(sender=sender, receiver_id=receiver_id, content=message)

        # Broadcast message to sender and receiver
        await self.channel_layer.group_send(
            f"chat_{receiver_id}",
            {
                "type": "chat_message",
                "message": message,
                "sender_id": sender.id,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        sender_id = event["sender_id"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender_id": sender_id}))


	# 	async def receive(self, text_data):
	# 		text_data_json = json.loads(text_data)
	# 		message = text_data_json['message']
	# 		receiver_username = text_data_json['receiver']
	# 		receiver = User.objects.get(username=receiver_username)
	# 		await self.save_message(self.user, receiver, message)
	# 		await self.send_message(receiver_username, message)
	
	# async def send_message(self, receiver_username, message):
	# 	await self.send(text_data=json.dumps({
	# 		'sender': self.user.username,
	# 		'receiver': receiver_username,
	# 		'message': message
	# 	}))
	
	# async def save_message(self, sender, receiver, message):
	# 	Message.objects.create(sender=sender, receiver=receiver, content=message)