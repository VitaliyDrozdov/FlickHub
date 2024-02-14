import datetime as dt
from rest_framework import serializers
from reviews.models import Category, Genre, Title, User, ROLES


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLES)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(many=True, slug_field='slug',
                                         queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('name', 'year', 'rating', 'description', 'genre', 'category')
        read_only_fields = ('rating',)

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('год выпуска не может быть'
                                              'больше текущего')
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
