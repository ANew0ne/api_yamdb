from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework import filters
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsAdminOrUserOrReadOnly


class CategoryGenreViewSet(CreateModelMixin, ListModelMixin,
                           DestroyModelMixin, GenericViewSet):
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'slug')
    permission_classes = (IsAdminOrUserOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'
