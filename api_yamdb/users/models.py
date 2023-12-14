from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models

from .enums import UserRole

MAX_FIELD_LENGTH = 150
MAX_EMAIL_LENGTH = 254


class User(AbstractUser):
    """Модель пользователя."""

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
                            default=UserRole.USER.value,
                            max_length=MAX_FIELD_LENGTH)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return (self.role == UserRole.ADMIN.value
                or self.is_superuser or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR.value

    @property
    def is_user(self):
        return self.role == UserRole.USER.value


class EmailVerification(models.Model):
    """Модель подтвердающего токена."""

    confirmation_code = models.CharField(max_length=6, unique=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='confirmation_code')

    def __str__(self):
        return f'EmailVerification for {self.user.email}'

    def send_verification_email(self):
        send_mail(
            'Подтверждение регистрации',
            f'Код подтверждения: {self.confirmation_code}',
            'from@example.com',
            [self.user.email],
            fail_silently=False,
        )
