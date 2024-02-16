
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import filters, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api_users.serializers import UserSerializer, SignUpSerializer
from api_users.permissions import IsAdminOnly, IsCurrentUserOnly

User = get_user_model()

class SignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def send_confirmation_email(self, user):
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Confirmation Code',
            message=f'Your confirmation code is: {confirmation_code}',
            from_email='from@example.com',
            recipient_list=[user.email],
            fail_silently=True
        )

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if User.objects.filter(username=request.data.get('username'), email=request.data.get('email')).exists():
            user = User.objects.get(username=request.data['username'], email=request.data['email'])
            self.send_confirmation_email(user)
            return Response({"detail": "User already exists. Confirmation email sent."}, status=status.HTTP_200_OK)
        else:
            if serializer.is_valid():
                user = serializer.save()
                self.send_confirmation_email(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
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


class AccessView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        user = authenticate(username=username, confirmation_code=confirmation_code)
        access_token = AccessToken.for_user(user)
        return Response({'access_token': str(access_token)}, status=status.HTTP_200_OK)
