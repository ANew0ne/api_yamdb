from django.contrib import admin

from .models import Review, Comment


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
