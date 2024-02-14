from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

ROLES = (
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
)


NAMES_MAX_LENGTH = 256
SLUG_MAX_LENGTH = 50

User = get_user_model()


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=16, choices=ROLES, default='user')


class AbstractCategoryGenreModel(models.Model):
    name = models.TextField(max_length=NAMES_MAX_LENGTH)
    slug = models.SlugField(
        unique=True,
        max_length=SLUG_MAX_LENGTH,
    )

    class Meta:
        abstract = True


class Category(AbstractCategoryGenreModel):
    pass


class Genre(AbstractCategoryGenreModel):
    pass


class Title(models.Model):
    name = models.TextField(max_length=NAMES_MAX_LENGTH)
    year = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(1300),
            validators.MaxValueValidator(2024),
        ],
    )
    rating = models.SmallIntegerField()  # needs change
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre,
                                   on_delete=models.SET_NULL,
                                   null=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True)
