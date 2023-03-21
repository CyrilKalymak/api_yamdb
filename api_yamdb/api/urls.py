from api.views import (CategoryViewSet,
                       GenreViewSet,
                       TitleViewSet,
                       ReviewViewSet,
                       CommentViewSet)
from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, confirmation_view, signup_view

v1_router = routers.DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register("titles", TitleViewSet, basename="titles")
v1_router.register("categories", CategoryViewSet, basename="categories")
v1_router.register("genres", GenreViewSet, basename="genres")
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path("v1/", include(v1_router.urls)),
    path('v1/auth/signup/', signup_view),
    path('v1/auth/token/', confirmation_view),
]
