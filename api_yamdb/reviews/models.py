from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

ROLES = (
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
)

class MyUser(AbstractUser):
    bio = models.TextField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=16, choices=ROLES, default='user')
    

User = get_user_model()

