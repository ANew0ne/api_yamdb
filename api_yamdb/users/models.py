from django.contrib.auth.models import AbstractUser
from django.db import models

from .enums import UserRole
MAX_LENGTH = 100


class User(AbstractUser):
    email = models.EmailField(verbose_name='Электронная почта',
                              unique=True,
                              max_length=MAX_LENGTH)
    username = models.CharField(verbose_name='Имя пользователя',
                                unique=True,
                                max_length=MAX_LENGTH)
    confirmation_code = models.CharField(max_length=MAX_LENGTH)
    role = models.CharField(verbose_name='Роль',
                            max_length=MAX_LENGTH,
                            choices=UserRole.choices(),
                            default=UserRole.USER)

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
