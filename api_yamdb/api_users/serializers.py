from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers


User = get_user_model()
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, allow_blank=False)
    username = serializers.CharField(max_length=150, allow_blank=False)
    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Пользователь с таким username уже существует.")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return data

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError("Username 'me' is not allowed.")
        
        return value

    class Meta:
        model = User
        fields = ('email', 'username',)
