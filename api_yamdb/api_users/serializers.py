from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers

from api_users.models import ROLES

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLES, required=False)

    def create(self, validated_data):
        role = validated_data.get('role', 'user')
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class SignupSerializer(serializers.ModelSerializer):
    def get_confirmation_code(self):
        return get_random_string(length=10)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError("Username 'me' is not allowed.")
        return value

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            email=validated_data['email'],
            defaults={'username': validated_data['username']}
        )
        return user
    class Meta:
        model = User
        fields = ('email', 'username',)
