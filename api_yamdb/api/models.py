from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=256)
    slug = models.SlugField(unique=True,
                            verbose_name='Слаг',
                            max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=256)
    slug = models.SlugField(unique=True,
                            verbose_name='Слаг',
                            max_length=50)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=256)
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(verbose_name='Описание', blank=True)
    genre = models.ManyToManyField(Genre,
                                   verbose_name='Жанр')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 verbose_name='Категория')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def clean(self):
        if self.year > timezone.now().year:
            raise ValidationError('Год выпуска не может быть больше текущего!')

    def __str__(self):
        return self.name