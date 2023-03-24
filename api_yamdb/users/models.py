from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Создание кастомного класса User, описание базовых функций"""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='Биография/О пользователе',
        help_text='Расскажите о себе'
    )

    role = models.CharField(
        max_length=max([len(role) for role, name in ROLES]),
        choices=ROLES,
        default=USER,
        verbose_name='Роль пользователя'
    )

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELDS = 'email'

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    def __str__(self):
        return self.username
