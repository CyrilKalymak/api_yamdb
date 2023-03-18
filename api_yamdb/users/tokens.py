from rest_framework_simplejwt.tokens import RefreshToken
from uuid import uuid1


def generate_user_confirm_code() -> str:
    return str(uuid1())


def get_user_jwt_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }
