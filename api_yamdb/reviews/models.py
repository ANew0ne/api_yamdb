from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models

from .validators import validate_year

User = get_user_model()

MAX_LENGTH = 256
TEXT_LIMIT_SHOW = 20
SLUG_LIMIT = 50


class CategoryGenreModel(models.Model):
    """Абстрактный класс с общими полями для Категории и Жанра."""
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг',
        max_length=SLUG_LIMIT
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class CommentReviewModel(models.Model):
    text = models.CharField(max_length=MAX_LENGTH)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        abstract = True


class Category(CategoryGenreModel):
    """Модель категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreModel):
    """Модель жанра произведений."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH,
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        db_index=True,
        validators=(validate_year,),
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(CommentReviewModel):
    """Модель Отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'validators': 'Диапазон от 1 до 10!'}
    )

    class Meta:
        default_related_name = 'reviews'
        ordering = ('author', '-pub_date',)
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


class Comment(CommentReviewModel):
    """Модель Комментариев."""

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
        ordering = ('-pub_date', 'author', )
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return (
            f'Review: {self.review[:TEXT_LIMIT_SHOW]}, '
            f'Text: {self.text[:TEXT_LIMIT_SHOW]}, '
            f'Author: {self.author}, '
            f'Date: {self.pub_date}, '
        )
