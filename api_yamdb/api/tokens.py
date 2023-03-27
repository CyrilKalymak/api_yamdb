from uuid import uuid1

from rest_framework_simplejwt.tokens import RefreshToken


def generate_user_confirm_code() -> str:
    return str(uuid1())


def get_user_jwt_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }
