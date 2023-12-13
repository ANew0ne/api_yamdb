from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import (IsAdminOnly, IsAdminOrUserOrReadOnly,
                          IsAdminOrModeratorOrAuthorOnly)
from .serializers import (CommentSerializer, ReviewSerializer,
                          CategorySerializer, GenreSerializer, TitleSerializer)
from reviews.models import Review, Title, Category, Genre


class UsersViewSet(viewsets.ModelViewSet):
    '''Вьюсет для Пользователя'''

    permission_classes = (IsAuthenticated, IsAdminOnly,)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вьюсет для Категорий'''

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'slug')
    permission_classes = (IsAdminOrUserOrReadOnly,)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вьюсет для Жанров'''

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'slug')
    permission_classes = (IsAdminOrUserOrReadOnly,)


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вьюсет для Произведений'''
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre', 'category')
    permission_classes = (IsAdminOrUserOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    '''Вьюсет для Комментариев'''

    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrModeratorOrAuthorOnly,)

    def get_review(self):
        return get_object_or_404(
            Review, id=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    '''Вьюсет для Отзывов'''

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrModeratorOrAuthorOnly,)

    def get_title(self):
        return get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
