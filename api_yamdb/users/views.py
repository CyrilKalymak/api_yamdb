from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (CreateUserSerializer, JWTTokenSerializer,
                          UsersSerializer)
from .permissions import IsAdmin
from .mixins import NoPutModelViewSet
from .utils import send_code

User = get_user_model()


class UsersViewSet(NoPutModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = UsersSerializer
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[permissions.IsAuthenticated],
            url_path='me', url_name='me')
    def me(self, request):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=self.request.user.role)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_user(request):
    if User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email')
    ).exists():
        send_code(
            User.objects.get(
                username=request.data.get('username'),
                email=request.data.get('email')
            ),
            request.data.get('email')
        )
        return Response(request.data, status=HTTPStatus.OK)
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    serializer.save()
    user = User.objects.get(email=email, username=username)
    send_code(user, email)
    return Response(serializer.data, status=HTTPStatus.OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer = JWTTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = serializer.validated_data.get('confirmation_code')
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, code):
        token = AccessToken.for_user(user)
        return Response(
            data={'token': token},
            status=HTTPStatus.OK
        )
    return Response(
        {code: 'Неверный код подтверждения'},
        status=HTTPStatus.BAD_REQUEST
    )
