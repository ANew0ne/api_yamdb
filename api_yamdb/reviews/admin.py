from django.contrib import admin

from .models import Review, Comment, Category, Genre, Title


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'score',
    )
    search_fields = (
        'pub_date',
        'author',
    )
    list_filter = (
        'pub_date',
        'author',
    )
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = (
        'review',
        'author',
    )
    list_filter = (
        'review',
        'author',
    )
    empty_value_display = '-пусто-'


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
