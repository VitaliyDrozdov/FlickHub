from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
NAMES_MAX_LENGTH = 256
SLUG_MAX_LENGTH = 50


class AbstractReviewModel(models.Model):
    author = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class AbstractCategoryGenreModel(models.Model):
    name = models.CharField(max_length=NAMES_MAX_LENGTH)
    slug = models.SlugField(
        unique=True,
        max_length=SLUG_MAX_LENGTH,
    )

    class Meta:
        abstract = True
        ordering = ('id',)

    def __str__(self):
        return self.slug
