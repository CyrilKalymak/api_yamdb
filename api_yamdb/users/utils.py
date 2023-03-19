from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator


def send_code(User, email):
    code = default_token_generator.make_token(
        User
    )
    email_message = f'Код подтверждения: {code}'
    send_mail(message=email_message,
              subject='Код подтвереждения',
              recipient_list=[email],
              from_email=settings.DEFAULT_FROM_EMAIL)
