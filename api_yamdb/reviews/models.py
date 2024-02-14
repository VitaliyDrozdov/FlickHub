from django.core import validators
from django.db import models
from django.utils import timezone

from .core_models import (
    AbstractReviewModel,
    AbstractCategoryGenreModel,
    NAMES_MAX_LENGTH,
)

MAX_COMMENT_LENGTH = 50


class Category(AbstractCategoryGenreModel):
    pass


class Genre(AbstractCategoryGenreModel):
    pass


class Title(models.Model):
    name = models.CharField(max_length=NAMES_MAX_LENGTH)
    year = models.PositiveSmallIntegerField(
        validators=[
            validators.MaxValueValidator(timezone.now().year),
        ],
    )
    rating = models.SmallIntegerField()  # needs change
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )


class GenreTitle(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True)
    genre_id = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)


class Review(AbstractReviewModel):
    text = models.TextField('Отзыв')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(10),
        ],
    )
    title = models.ForeignKey(
        Title, verbose_name='Название', on_delete=models.CASCADE
    )

    class Meta(AbstractReviewModel.Meta):
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'), name='unique_title_review'
            )
        ]
        default_related_name = 'reviews'

    def __str__(self):
        return self.text[:MAX_COMMENT_LENGTH]


class Comment(AbstractReviewModel):
    text = models.TextField('Комментарий')
    review = models.ForeignKey(
        Review, verbose_name='Обзор', on_delete=models.CASCADE
    )

    class Meta(AbstractReviewModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:MAX_COMMENT_LENGTH]
