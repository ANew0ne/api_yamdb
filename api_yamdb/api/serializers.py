from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import (Comment, Title, Review,
                            Category, Genre)
from users.models import User

MIN_VALUE = 0
MAX_VALUE = 10


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if MIN_VALUE > value > MAX_VALUE:
            raise serializers.ValidationError('Диапазон значений от 1 до 10!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Нельзя дублировать отзыв!')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug', many=True,
                                         queryset=Genre.objects.all())

    class Meta:
        model = Title
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализация запроса и ответа для регистрации пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields[self.username_field] = serializers.CharField()
#         self.fields['password'] = user.confirmation_code
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     token['username'] = user.username
    #     token['confirmation_code'] = user.confirmation_code

    #     return token
# class GetTokenSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(
#         required=True)
#     confirmation_code = serializers.CharField(
#         required=True)

#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'confirmation_code'
#         )
