from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api_users.permissions import IsAdminOnly, IsCurrentUserOnly
from api_users.serializers import (
    SignUpSerializer,
    TokenSerializer,
    UserProfileSerializer,
    UserSerializer,
)

User = get_user_model()


class SignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, created = User.objects.get_or_create(
            **serializer.validated_data
            )
        except IntegrityError:
            return Response(
                {"username": "пользователь с таким username уже существует.",
                 "email": "пользователь с таким email уже существует."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.send_confirmation_email(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccessView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """Создает access_token для пользователя."""
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data.get('username')
        )
        access_token = AccessToken.for_user(user)
        return Response(
            {'token': str(access_token)}, status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    permission_classes = (IsAdminOnly,)
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
        'head',
        'options',
        'trace',
    ]

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(IsCurrentUserOnly,),
    )
    def get_profile(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UserProfileSerializer(
            self.request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
