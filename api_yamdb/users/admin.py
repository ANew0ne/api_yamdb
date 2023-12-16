from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(UserAdmin):
    """Административный класс для управления пользователями."""

    list_display = (
        'username',
        'email',
        'role',
        'is_active',
    )
    search_fields = ('username',)
    list_filter = ('role',)
    empty_value_display = '-пусто-'
