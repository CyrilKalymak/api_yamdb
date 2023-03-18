from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('me зарегистрировано системой')
        return value

    def validate_email(self, value):
        norm_email = value.lower()
        if User.objects.filter(email=norm_email).exists():
            raise serializers.ValidationError('Email уже зарегистрирован')
        return norm_email


class CreateUserSerializer(UsersSerializer):
    class Meta:
        fields = ('username', 'email')
        model = User


class JWTTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField()
    username = serializers.CharField()
