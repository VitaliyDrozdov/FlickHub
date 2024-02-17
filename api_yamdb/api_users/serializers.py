from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')


class UserProfileSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError("Username 'me' is not allowed.")
        return value

    class Meta:
        model = User
        fields = ('email', 'username',)


class TokenSerializer(serializers.ModelSerializer):

    def validate_confirmation_code(self, value):
        username = self.context.get('username')
        user = get_object_or_404(User, username=username)
        check = default_token_generator.check_token(user, value)
        if not check:
            raise ValidationError('Неверный код подтверждения')
        return value

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)
