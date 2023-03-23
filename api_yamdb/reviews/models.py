from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User
from api.validators import spell_slug

import datetime as dt

class Category(models.Model):

    name = models.CharField(max_length=256,
                            verbose_name='Название категории')
    slug = models.SlugField(max_length=50,
                            verbose_name='Идентификатор категории',
                            unique=True,
                            validators=[spell_slug])
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название жанра')
    slug = models.SlugField(max_length=50,
                            verbose_name='Идентификатор жанра',
                            unique=True,
                           validators=[spell_slug])
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название произведения')
    year = models.PositiveIntegerField(verbose_name='год выпуска',
        validators=[
            MinValueValidator(
                0, message='Год не может быть отрицательным.'
            ),
            MaxValueValidator(
                int(dt.datetime.now().year),
                message='Произведение нельзя создать в будущем году.'
            )
        ],
        db_index=True)
    description = models.TextField(verbose_name='Описание произведения',
                                   blank=True, null=True)
    category = models.ForeignKey(Category, related_name='categories',
                                 on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle',
                                    related_name='titles')
    
    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL,
                              null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}: {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1, "Минимальная оценка - 1"),
        MaxValueValidator(10, "Максимальная оценка - 10"),
    ],
        verbose_name='Рейтинг',

    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='uniqueConstraint_review'
            ),
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.text
