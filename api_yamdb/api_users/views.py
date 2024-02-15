from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import filters, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken


from api_users.serializers import UserSerializer, SignupSerializer
# from api_users.permissions import IsAdminOnly

User = get_user_model()

class SignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = serializer.get_confirmation_code()
            user = serializer.save()
            send_mail(
                subject='Confirmation Code',
                message=f'Your confirmation code is: {confirmation_code}',
                from_email='from@example.com',
                recipient_list=[user.email],
                fail_silently=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    # permission_classes = (permissions.AllowAny,)


    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def get_profile(self, request):
    # permission_classes = (IsAuthenticated,)
        profile = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
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
        # if user is None:
        #     return Response({'error': 'Invalid username or confirmation code'}, status=status.HTTP_400_BAD_REQUEST)
        access_token = AccessToken.for_user(user)
        return Response({'access_token': str(access_token)}, status=status.HTTP_200_OK)
