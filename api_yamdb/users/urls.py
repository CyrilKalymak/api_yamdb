from django.urls import path
from api.views import confirmation_view, signup_view

app_name = 'users'

urlpatterns = [
    path('signup/', signup_view, name='signup_view'),
    path('token/', confirmation_view, name='confirmation_view'),
]
