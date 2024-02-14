from rest_framework import filters, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from api_users.serializers import UserSerializer
from api_users.models import User
from api_users.permissions import IsAdminOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    # permission_classes = (IsAdminOnly,)

    
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

# def get_permissions(self):
#         if self.action != 'get_profile':
#             return (IsAdminOnly,)
#         return (IsMeOrReadOnly,)