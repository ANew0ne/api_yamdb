from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from .serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review, Title


class CommentViewSet(viewsets.ModelViewSet):
    '''Вьюсет для Комментариев'''

    serializer_class = CommentSerializer
    # permission_classes =

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
    # permission_classes =

    def get_title(self):
        return get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
