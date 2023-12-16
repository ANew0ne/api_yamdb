from django.db.models import TextChoices


class UserRole(TextChoices):
    ADMIN = ('admin', 'admin')
    USER = ('user', 'user')
    MODERATOR = ('moderator', 'moderator')
