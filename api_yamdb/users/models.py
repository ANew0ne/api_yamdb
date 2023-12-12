from django.contrib.auth.models import AbstractUser
from django.db import models

from .enums import UserRole
MAX_FIELD_LENGTH = 150
MAX_EMAIL_LENGTH = 254


class User(AbstractUser):
    email = models.EmailField(verbose_name='Электронная почта',
                              unique=True,
                              max_length=MAX_EMAIL_LENGTH)
    username = models.CharField(verbose_name='Имя пользователя',
                                unique=True,
                                max_length=MAX_FIELD_LENGTH)
    first_name = models.CharField(verbose_name='Имя',
                                  max_length=MAX_FIELD_LENGTH,
                                  null=True, blank=True)
    last_name = models.CharField(verbose_name='Фамилия',
                                 max_length=MAX_FIELD_LENGTH,
                                 null=True, blank=True)
    bio = models.TextField(verbose_name='О себе',
                           null=True, blank=True)
    role = models.CharField(verbose_name='Роль',
                            choices=UserRole.choices(),
                            default=UserRole.USER,
                            max_length=MAX_FIELD_LENGTH)

    REQUIRED_FIELDS = ('email',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('last_name', 'first_name')

    @property
    def is_admin(self):
        return (self.role == UserRole.ADMIN.value
                or self.is_superuser or self.is_stuff)

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR.value

    @property
    def is_user(self):
        return self.role == UserRole.USER.value
