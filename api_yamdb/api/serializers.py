import datetime as dt
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment


# region Titles
class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(many=True, slug_field='slug',
                                         queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())
    rating = serializers.IntegerField(read_only=True, source='get_rating')

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('год выпуска не может быть'
                                              'больше текущего')
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


# endregion


# region Review
class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, attrs):
        if not self.context.get('request').method == 'POST':
            return attrs
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError('The review already exists.')
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


# endregion
