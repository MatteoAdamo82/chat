from django.contrib import admin

from .models import Room, ChatUser


admin.site.register([
    Room,
    ChatUser,
])