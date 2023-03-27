from api.views import confirmation_view, signup_view
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('signup/', signup_view, name='signup_view'),
    path('token/', confirmation_view, name='confirmation_view'),
]
