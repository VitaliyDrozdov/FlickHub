from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = (
    (ADMIN, 'Администратор'),
    (USER, 'Аутентифицированный пользователь'),
    (MODERATOR, 'Модератор'),
)


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        validators=[UnicodeUsernameValidator()],
    )
    email = models.EmailField(unique=True)
    bio = models.TextField('Биография', max_length=255, blank=True)
    role = models.CharField('Роль', max_length=30, choices=ROLES, default=USER)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_user(self):
        return self.role == USER

    def __str__(self) -> str:
        return self.username
