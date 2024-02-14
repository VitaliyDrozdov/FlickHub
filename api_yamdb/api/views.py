from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, UserSerializer)
from api.permissions import AdminOrReadOnly
from reviews.models import Category, Genre, Title, User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    # Пока временно сделал так для создания, т.к. не разобрался еще. Позже заменю.
    def perform_create(self, serializer):
        serializer.save(username=self.request.user.username)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')


class AbstractCategoryGenreViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)


class CategoryViewSet(AbstractCategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(AbstractCategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
