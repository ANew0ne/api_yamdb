from django.contrib.auth.models import AbstractUser
from django.db import models

from users.enums import UserRole
from users.validators import validate_username

MAX_FIELD_LENGTH = 150
MAX_EMAIL_LENGTH = 254


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        max_length=MAX_EMAIL_LENGTH
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=MAX_FIELD_LENGTH,
        validators=(validate_username,)
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=MAX_FIELD_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=MAX_FIELD_LENGTH,
        blank=True
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=UserRole.choices,
        default=UserRole.USER.value,
        max_length=MAX_FIELD_LENGTH
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('date_joined',)

    @property
    def is_admin(self):
        return (self.role == UserRole.ADMIN.value
                or self.is_superuser or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR.value
