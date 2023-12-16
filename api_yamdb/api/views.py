from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, UpdateModelMixin,
                                   RetrieveModelMixin, ListModelMixin,
                                   DestroyModelMixin)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .mixins import ModelMixinSet
from api.permissions import (IsAdminOnly, IsAdminOrUserOrReadOnly,
                             IsAdminOrModeratorOrAuthorOnly)
from api.serializers import (CommentSerializer, ReviewSerializer,
                             SignUpSerializer, CategorySerializer,
                             GenreSerializer, TitleSerializer,
                             TitleGetSerializer,
                             TokenSerializer, UsersSerilizer,
                             UsersSerilizerForAdmin)
from reviews.models import Review, Title, Category, Genre
from users.models import User
from api.filters import TitleFilter
from api_yamdb.settings import EMAIL_HOST_USER


class UsersViewSet(viewsets.ModelViewSet):
    """Вьюсет для Пользователя."""

    queryset = User.objects.all()
    serializer_class = UsersSerilizerForAdmin
    permission_classes = (IsAuthenticated, IsAdminOnly,)
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ('username',)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = (
        "get",
        "post",
        "patch",
        "delete",
    )

    @action(detail=False,
            methods=('GET', 'PATCH'),
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        if request.method == "PATCH":
            serializer = UsersSerilizer(request.user,
                                        data=request.data,
                                        partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'GET':
            serializer = UsersSerilizer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryViewSet(ModelMixinSet):
    """Вьюсет для Категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class GenreViewSet(ModelMixinSet):
    """Вьюсет для Жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class TitleViewSet(GenericViewSet, CreateModelMixin, UpdateModelMixin,
                   RetrieveModelMixin, ListModelMixin,
                   DestroyModelMixin):
    """Вьюсет для Произведений."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrUserOrReadOnly,)
    http_method_names = ('get', 'post', 'delete', 'patch',)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleGetSerializer
        return TitleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для Комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrModeratorOrAuthorOnly,)
    http_method_names = ('get', 'post', 'delete', 'patch',)

    def get_review(self):
        return get_object_or_404(
            Review, id=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для Отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrModeratorOrAuthorOnly,)
    http_method_names = ('get', 'post', 'delete', 'patch',)

    def get_title(self):
        return get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class SignUpView(APIView):
    """Вьюсет для регистрации пользователя."""

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса."""
        serializer = SignUpSerializer(data=request.data)
        if User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).exists():
            return Response(request.data, status=status.HTTP_200_OK)
        if serializer.is_valid():
            user = serializer.save()
            send_mail(
                'Подтверждение регистрации',
                'Код подтверждения: '
                f'{default_token_generator.make_token(user)}',
                EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainTokenView(APIView):
    """Вьюсет для получения токена."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User,
                                 username=serializer.data.get('username'))
        confirmation_code = serializer.data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK
            )
        return Response('Invalid token!',
                        status=status.HTTP_400_BAD_REQUEST)
