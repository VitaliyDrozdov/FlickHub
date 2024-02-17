from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets


from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleGetSerializer,
    TitlePostPatchSerializer,
    ReviewSerializer,
    CommentSerializer,
)
from api.filters import TitleFilterSet
from api.permissions import IsAdminOrReadOnly,IsAuthorModeratorAdminOrReadOnly
from reviews.models import Category, Genre, Title, Review


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TitleGetSerializer
        return TitlePostPatchSerializer


class CategoryGenreViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorModeratorAdminOrReadOnly]
    http_method_names = ['get', 'post', 'delete', 'patch']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        # return Review.objects.filter(title=self.kwargs['title_id'])
        return self.get_title().reviews.all()

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorModeratorAdminOrReadOnly]
    http_method_names = ['get', 'post', 'delete', 'patch']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def get_queryset(self):
        return self.get_review().comments.all()

    def get_review(self):
        return get_object_or_404(
            Review, pk=self.kwargs['review_id'], title=self.kwargs['title_id']
        )
