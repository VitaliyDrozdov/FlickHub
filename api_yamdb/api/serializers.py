from rest_framework import serializers
from reviews.models import User, ROLES


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLES)
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
