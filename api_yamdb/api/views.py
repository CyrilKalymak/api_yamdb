from http import HTTPStatus

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from api.permissions import IsAdmin
from users.models import User
from reviews.models import Category, Genre, Title, Review
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          ReviewSerializer,
                          CommentSerializer,
                          GetTokenSerializer,
                          SignUpSerializer,
                          UserSerializer)
from rest_framework.pagination import LimitOffsetPagination
from .permissions import (IsAdminOrReadOnly,
                          IsAdminOrOwnerOrReadOnly,
                          IsAuthorOrIsModeratorOrAdminOrReadOnly)


class TitleViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')


class CategoryViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class GenreViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


@api_view(['POST'])
def signup_view(request):
    """Функция для получения кода авторизации на почту."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    try:
        new_user, created = User.objects.get_or_create(
            username=username,
            email=email,
        )
    except IntegrityError:
        error = settings.USERNAME_ERROR if User.objects.filter(
            username=username).exists() else settings.EMAIL_ERROR
        return Response(error, status=HTTPStatus.BAD_REQUEST)

    confirmation_code = default_token_generator.make_token(new_user)
    send_mail(
        subject='Код подтверждения',
        message=f'Регистрация прошла успешно! '
                f'Код подтверждения: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False
    )
    return Response(serializer.data, status=HTTPStatus.OK)


@api_view(['POST'])
def confirmation_view(request):
    """Функция для получения токена."""
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = serializer.validated_data.get('confirmation_code')
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, code):
        response = {'Неверный код'}
        return Response(response, status=HTTPStatus.BAD_REQUEST)
    token = str(RefreshToken.for_user(user).access_token)
    response = {'token': token}
    return Response(response, status=HTTPStatus.OK)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = [IsAdmin, ]
    search_fields = ('username',)
    filter_backends = (filters.SearchFilter,)

    @action(detail=False, permission_classes=[IsAuthenticated],
            methods=['GET', 'PATCH'], url_path='me')
    def get_or_update_self(self, request):
        """Редактирование и получение информации профиля."""
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data,
                            status=HTTPStatus.OK)
        if request.method == 'PATCH':
            serializer = UserSerializer(user,
                                        data=request.data,
                                        partial=True, )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
            return Response(serializer.data,
                            status=HTTPStatus.OK)
