from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь')
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    email = models.EmailField(
        verbose_name='E-mail',
        null=False,
        blank=False,
        max_length=254,
        unique=True
    )
    role = models.CharField(
        max_length=settings.DEFAULT_FIELD_SIZE,
        choices=ROLES,
        default=USER,
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='username_email'
            ),
        ]

    def clean(self):
        if self.username == 'me':
            raise ValidationError('Имя me недоступно для регистрации')
        super(User, self).clean()

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
