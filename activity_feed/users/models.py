from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.TextField('Био', blank=True)
    avatar = models.ImageField('Аватарка', upload_to='avatars', blank=True)
