from rest_framework import serializers

from .models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='category',
                                            queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(slug_field='genre', many=True,
                                         queryset=Genre.objects.all())

    class Meta:
        model = Title
        fields = '__all__'
