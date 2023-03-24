from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import UserViewSet, confirmation_view, signup_view


app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)

urlpatterns_auth = [
    path('signup/', confirmation_view.as_view(), name='signup'),
    path('token/', confirmation_view.as_view(), name='token'),
]


urlpatterns = [
    path('v1/auth/', include(urlpatterns_auth)),
]
