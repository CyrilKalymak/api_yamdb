from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
# from users.views import SignUp
from django.urls import include, path
from rest_framework import routers


v1_router = routers.DefaultRouter()
v1_router.register("titles", TitleViewSet, basename="titles")
v1_router.register("categories", CategoryViewSet, basename="categories")
v1_router.register("genres", GenreViewSet, basename="genres")

urlpatterns = [
    path("v1/", include(v1_router.urls)),
    path("v1/", include("djoser.urls.jwt")),
    path("v1/", include("users.urls")),
]
