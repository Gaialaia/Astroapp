from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from hashlib import md5

class CustomUser(AbstractUser):
    objects = UserManager()

    email = models.EmailField(unique=True)

    description = models.TextField(max_length=600, default='', blank=True)
    birthdate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.username}'

    def make_avatar(self, size=128):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'



