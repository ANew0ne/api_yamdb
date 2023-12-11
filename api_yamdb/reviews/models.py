from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.model import User

MAX_LENGTH = 200
TEXT_LIMIT_SHOW = 20


class Review(models.Model):
    '''Модель Отзывов'''
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    text = models.CharField(
        max_length=MAX_LENGTH
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.IntegerField(
        'Оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'validators': 'Диапазон от 1 до 10!'}
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        default_related_name = 'reviews'
        ordering = ('author', '-pub_date')
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique review'
            )]

    def __str__(self):
        return (
            f'Title: {self.title[:TEXT_LIMIT_SHOW]}, '
            f'Text: {self.text[:TEXT_LIMIT_SHOW]}, '
            f'Author: {self.author}, '
            f'Date: {self.pub_date}, '
            f'Score: {self.score}'
        )


class Comment(models.Model):
    '''Модель Комментариев'''

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    text = models.CharField(
        'Текст комментария',
        max_length=MAX_LENGTH
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        default_related_name = 'comments'
        ordering = ('author', '-pub_date')
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return (
            f'Review: {self.review[:TEXT_LIMIT_SHOW]}, '
            f'Text: {self.text[:TEXT_LIMIT_SHOW]}, '
            f'Author: {self.author}, '
            f'Date: {self.pub_date}, '
        )
