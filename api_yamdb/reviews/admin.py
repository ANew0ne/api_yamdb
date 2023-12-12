from django.contrib import admin

from .models import Category, Genre, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description',
                    'display_genre', 'category')
    list_filter = ('name', 'year', 'genre', 'category')
    empty_value_display = '-пусто-'

    def display_genre(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])
    display_genre.short_description = 'Жанр'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug'
    )
    list_filter = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug'
    )
    list_filter = ('name', 'slug')
