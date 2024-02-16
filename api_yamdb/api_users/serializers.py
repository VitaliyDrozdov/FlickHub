from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator


User = get_user_model()
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class SignUpSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError("Username 'me' is not allowed.")
        return value
    class Meta:
        model = User
        fields = ('email', 'username',)
