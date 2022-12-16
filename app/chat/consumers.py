import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Room, ChatUser
from urllib.parse import parse_qs
from django.core.serializers.json import DjangoJSONEncoder

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        qs = parse_qs(self.scope['query_string'])
        username = qs.get(b'username')[0].decode()
        is_added = await self.add_user_in_room(
            username,
            qs.get(b'gender')[0].decode(),
            qs.get(b'age')[0].decode(),
            qs.get(b'uuid')[0].decode(),
            self.room_name
        )

        if is_added == True:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

            users_list = await self.get_json_users_list(self.room_name)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'username': username,
                    'users_list': users_list
                }
            )

        else:
            await self.close()
 
    async def disconnect(self, close_code):
        qs = parse_qs(self.scope['query_string'])
        username=qs.get(b'username')[0].decode()

        removed = await self.remove_user_from_room(
                username,
                qs.get(b'uuid')[0].decode(),
                self.room_name
            )
        if removed == True:
            users_list = await self.get_json_users_list(self.room_name)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'username': username,
                    'users_list': users_list
                }
            )

            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': data['message'],
                'username': data['username'],
                'room': data['room']
            }
        )

    async def user_join(self, event):
        await self.send(text_data=json.dumps(event))
        
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_leave(self, event):
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def add_user_in_room(self, username, gender, age, uuid, room_slug):
        room = Room.objects.get(slug=room_slug)
        if not room.is_user_logged_in(username=username):
            user = ChatUser()
            user.username = username
            user.gender = gender
            user.age = age
            user.roomSlug = room_slug
            user.uuid = uuid
            user.save()
            room.join(chatuser=user)

            self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'user': username,
                }
            )

            return True

        return False

    @sync_to_async
    def remove_user_from_room(self, username, uuid, room_slug):
        room = Room.objects.get(slug=room_slug)
        try:
            user = ChatUser.objects.get(
                username=username,
                roomSlug=room_slug,
                uuid=uuid
            )
        except ChatUser.DoesNotExist:
            user = None
        
        if (user):
            room.leave(user)
            user.delete()

            return True
        
        return False

    @sync_to_async
    def get_json_users_list(self, room_slug):
        room = Room.objects.get(slug=room_slug)
        results = room.online.values_list('username', 'gender', 'age')

        return json.dumps(list(results), cls=DjangoJSONEncoder)
