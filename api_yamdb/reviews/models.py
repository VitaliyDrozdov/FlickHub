from django.core import validators
from django.db import models
from django.contrib.auth import get_user_model

MAX_COMMENT_LENGTH = 50

User = get_user_model()


class AbstractReviewModel(models.Model):
    author = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class Title(models.Model):
    pass


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
        'Title', verbose_name='Название', on_delete=models.CASCADE
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
