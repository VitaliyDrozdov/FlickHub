
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api_users.permissions import IsAdminOnly, IsCurrentUserOnly
from api_users.serializers import (SignUpSerializer, TokenSerializer,
                                   UserSerializer)

User = get_user_model()

class SignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def send_confirmation_email(self, user):
        """
        Отправляет confirmation_code пользователю и сохраняет его в БД.
        """
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            subject='Confirmation Code',
            message=f'Your confirmation code is: {confirmation_code}',
            from_email='from@example.com',
            recipient_list=[user.email],
            fail_silently=True
        )

    def post(self, request, *args, **kwargs):
        """
       Проверяет, существует ли пользователь в БД. Если да, то получает объект пользователя
       и отправляет confirmation_code на email;
       Если не существует - создает нового пользователи и отправляет confirmation_code на email.
        """
        serializer = SignUpSerializer(data=request.data)
        if User.objects.filter(username=request.data.get('username'), email=request.data.get('email')).exists():
            user = User.objects.get(username=request.data['username'], email=request.data['email'])
            self.send_confirmation_email(user)
            return Response({"detail": "Пользватель уже существует. Новый сonfirmation_code отаправлен на почту."}, status=status.HTTP_200_OK)
        else:
            if serializer.is_valid():
                user = serializer.save()
                self.send_confirmation_email(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccessView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Проверяет, передан ли username в request. Создает access_token для пользователя.
        """
        username = request.data.get('username')
        if not username:
            return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TokenSerializer(data=request.data, context={'username': username})
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(User, username=serializer.validated_data['username'])
            access_token = AccessToken.for_user(user)
            return Response({'token': str(access_token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    permission_classes = (IsAdminOnly,)


    @action(detail=False, methods=['get', 'patch'], url_path='me', permission_classes=(IsCurrentUserOnly,))
    def get_profile(self, request):
        profile = get_object_or_404(User, username=self.request.user.username)
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


