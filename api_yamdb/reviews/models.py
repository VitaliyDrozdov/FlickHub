from django.core import validators
from django.db import models


NAMES_MAX_LENGTH = 256
SLUG_MAX_LENGTH = 50


class AbstractCategoryGenreModel(models.Model):
    name = models.TextField(max_length=NAMES_MAX_LENGTH)
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг',
        max_length=SLUG_MAX_LENGTH,
    )


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
