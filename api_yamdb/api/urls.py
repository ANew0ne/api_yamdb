from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ReviewViewSet, CommentViewSet, SignUpView,
                    CategoryViewSet, GenreViewSet, TitleViewSet,
                    ObtainTokenView, UsersViewSet)

router_v1 = DefaultRouter()

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register('users', UsersViewSet, basename='users')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')

auth_urls = [
    path('token/',
         ObtainTokenView.as_view(),
         name='token_obtain_pair'),
    path('signup/',
         SignUpView.as_view(),
         name='auth_signup')
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_urls))
]
