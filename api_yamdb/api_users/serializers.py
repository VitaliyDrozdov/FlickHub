from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api_yamdb.settings import EMAIL_SENDER

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserProfileSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True, validators=[UnicodeUsernameValidator()])

    def send_confirmation_email(self, user):
        """Отправляет confirmation_code пользователю."""
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Confirmation Code',
            message=f'Your confirmation code is: {confirmation_code}',
            from_email=EMAIL_SENDER,
            recipient_list=[user.email],
            fail_silently=True,
        )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError('Username \'me\' is not allowed.')
        return value

    class Meta:
        model = User
        fields = ('email', 'username',)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, allow_blank=False)

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs.get('username'))
        confirmation_code = default_token_generator.make_token(user)
        if confirmation_code != attrs.get('confirmation_code'):
            raise ValidationError('Неверный код подтвеждения.')
        return attrs

    class Meta:
        model = User
        fields = ('username',)
