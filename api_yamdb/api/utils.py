from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def send_code(user, email):
    code = default_token_generator.make_token(
        user
    )
    send_mail(message=f'Код подтверждения: {code}',
              subject='Код подтвереждения',
              recipient_list=[email],
              from_email=settings.DEFAULT_FROM_EMAIL)
