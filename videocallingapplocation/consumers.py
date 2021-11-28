# Synchronous Code
# # chat/consumers.py
# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name'] #Get room name from url router in routing.py
#         self.group_room_name = "room_"+self.room_name
#         async_to_sync(self.channel_layer.group_add)(self.group_room_name,self.channel_name) #Join room group
#         self.accept()

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(self.group_room_name,self.channel_name)

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         async_to_sync(self.channel_layer.group_send)(
#             self.group_room_name,
#             {
#                 'type': 'groupmember_receive_message',
#                 'message': message
#             }
#         )

#     def groupmember_receive_message(self, event):
#         message = event['message']
#         self.send(json.dumps(
#             {"message": message}
#         ))

#Asynchronous Code
# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] #Get room name from url router in routing.py
        self.group_room_name = "room_"+self.room_name
        await self.channel_layer.group_add(self.group_room_name,self.channel_name) #Join room group
        await self.accept()
        await self.channel_layer.group_send(
            self.group_room_name,
            {
                'type': 'groupmember_receive_message',
                'message': self.channel_name + " was added to the group."
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.group_room_name,
            {
                'type': 'groupmember_receive_message',
                'message': self.channel_name + " left the group."
            }
        )
        await self.channel_layer.group_discard(self.group_room_name,self.channel_name) 

    async def receive(self, text_data):
        print("REEIVED MESSAGE:",text_data)
        text_data_json = json.loads(text_data)
        user = text_data_json['user']
        print(user)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.group_room_name,
            {
                'type': 'groupmember_receive_message',
                'message': user + ": " + message
            }
        )
    async def groupmember_receive_message(self, event):
        message = event['message']
        await self.send(json.dumps(
            {"message": message}
        ))
