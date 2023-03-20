from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment
from users.models import User
from .validators import username_validator

import datetime as dt


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError(
                'Проверьте год создания произведения.'
            )
        return value

    def create(self, validated_data):
        if 'genres' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title
        else:
            genres = validated_data.pop('genres')
            title = Title.objects.create(**validated_data)
            for genre in genres:
                current_genre, status = Genre.objects.get_or_create(
                    **genre)
                GenreTitle.objects.create(
                    genre=current_genre, title=title)
            return title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )
    title = serializers.SlugRelatedField(
        slug_field="id",
        many=False,
        read_only=True
    )

    class Meta:
        fields = "__all__"
        model = Review

    def validate(self, data):
        if self.context["request"].method != "POST":
            return data
        title = get_object_or_404(
            Title,
            pk=self.context["view"].kwargs.get("title_id")
        )
        author = self.context["request"].user
        if Review.objects.filter(title_id=title, author=author).exists():
            raise serializers.ValidationError(
                "Вы уже оставляли обзор на данное произведение"
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    review = serializers.SlugRelatedField(read_only=True, slug_field="text")

    class Meta:
        fields = "__all__"
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('username', 'email'),
                message=('Пользователь с таким email уже существует')
            )
        ]


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=settings.FIELD_EMAIL_LENGTH)
    username = serializers.CharField(max_length=settings.FIELD_MAX_LENGTH,
                                     validators=[username_validator])

    class Meta:
        model = User
        fields = ('email', 'username')


class GetTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField(
        max_length=settings.FIELD_TOKEN_LENGTH,
        validators=[username_validator]
    )
    confirmation_code = serializers.CharField(
        max_length=settings.FIELD_TOKEN_LENGTH, write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )
