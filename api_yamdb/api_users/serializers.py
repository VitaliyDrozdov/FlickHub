from rest_framework import serializers
from api_users.models import User, ROLES


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=150)
    # email = serializers.CharField(max_length=255)
    role = serializers.ChoiceField(choices=ROLES)
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')

