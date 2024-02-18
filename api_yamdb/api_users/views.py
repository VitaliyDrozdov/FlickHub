from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q
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

    def send_confirmation_email(self, user):
        """Отправляет confirmation_code пользователю и сохраняет его в БД."""
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Confirmation Code',
            message=f'Your confirmation code is: {confirmation_code}',
            from_email='from@example.com',
            recipient_list=[user.email],
            fail_silently=True,
        )

    def post(self, request, *args, **kwargs):
        """
        Проверяет, существует ли пользователь в БД,
        отправляет confirmation_code на email.
        """
        serializer = SignUpSerializer(data=request.data)
        user_query = Q(
            username=request.data.get('username'),
            email=request.data.get('email'),
        )
        if User.objects.filter(user_query).exists():
            user = User.objects.get(user_query)
            self.send_confirmation_email(user)
            return Response(serializer.initial_data, status=status.HTTP_200_OK)

        if serializer.is_valid():
            user = serializer.save()
            self.send_confirmation_email(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccessView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """Создает access_token для пользователя."""
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, username=serializer.validated_data.get('username')
            )
            access_token = AccessToken.for_user(user)
            return Response(
                {'token': str(access_token)}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
