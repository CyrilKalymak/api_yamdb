from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Category, Genre, Title, Review
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          ReviewSerializer,
                          CommentSerializer)
from rest_framework.pagination import LimitOffsetPagination
from .permissions import (IsAdminOrReadOnly,
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
    permission_classes = [IsAuthorOrIsModeratorOrAdminOrReadOnly, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrIsModeratorOrAdminOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
