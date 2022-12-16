from django.db import models
from . import validators
from django.core.validators import MaxValueValidator, MinValueValidator

class ChatUser(models.Model):
    username = models.CharField(max_length=30, validators=[validators.validate_username])
    roomSlug = models.CharField(max_length=30, blank=False)
    gender = models.SmallIntegerField(default=0,validators=[MaxValueValidator(2), MinValueValidator(0)])
    age = models.SmallIntegerField(default=0,validators=[MaxValueValidator(99), MinValueValidator(18)])
    uuid = models.UUIDField()
    class Meta:
        unique_together = ('username', 'roomSlug')

    def __str__(self):
        return self.username
class Room(models.Model):
    name = models.CharField(max_length=30)
    slug = models.CharField(max_length=30, unique=True, validators=[validators.validate_room_slug])
    online = models.ManyToManyField(to=ChatUser, blank=True)

    def join(self, chatuser):
        self.online.add(chatuser)
        self.save()

    def leave(self, chatuser):
        self.online.remove(chatuser)
        self.save()

    def get_online_count(self):
        return self.online.count()

    def is_user_logged_in(self, username):
        users = self.online.all()
        for user in users:
            if user.username == username:
                return True
        return False

    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'
