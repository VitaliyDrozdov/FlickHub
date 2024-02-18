from django.db import models

from reviews.core_models import (
    AbstractReviewModel,
    AbstractCategoryGenreModel,
    NAMES_MAX_LENGTH,
)
from reviews.validators import year_validator, rating_validator

MAX_COMMENT_LENGTH = 50


class Category(AbstractCategoryGenreModel):
    class Meta(AbstractCategoryGenreModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(AbstractCategoryGenreModel):
    class Meta(AbstractCategoryGenreModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField('Название', max_length=NAMES_MAX_LENGTH)
    year = models.PositiveSmallIntegerField(
        'Год',
        validators=[year_validator],
    )
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанры',
                                   through='GenreTitle')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, verbose_name='Категория',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('id',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)


class Review(AbstractReviewModel):
    text = models.TextField('Отзыв')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[rating_validator],
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Название',
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta(AbstractReviewModel.Meta):
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'), name='unique_title_review'
            )
        ]

    def __str__(self):
        return self.text[:MAX_COMMENT_LENGTH]


class Comment(AbstractReviewModel):
    text = models.TextField('Комментарий')
    review = models.ForeignKey(
        Review,
        verbose_name='Обзор',
        on_delete=models.CASCADE,
        related_name='comments',
    )

    class Meta(AbstractReviewModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:MAX_COMMENT_LENGTH]
