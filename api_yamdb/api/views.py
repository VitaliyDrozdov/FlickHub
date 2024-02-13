from rest_framework import filters, permissions, viewsets

from api.serializers import UserSerializer
from reviews.models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    
    
    def perform_create(self, serializer):
        serializer.save(username=self.request.user.username)
        

