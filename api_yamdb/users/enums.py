from django.db.models import TextChoices


class UserRole(TextChoices):
    ADMIN = ('admin',)
    USER = ('user',)
    MODERATOR = ('moderator',)
