from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from api_users.models import User, ROLES

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLES, required=False)
    
    def create(self, validated_data):
        role = validated_data.get('role', 'user')
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')

