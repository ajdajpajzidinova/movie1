from rest_framework import serializers
from .models import (
    UserProfile, Category, Genre,
    Country, Director, Actor, Movie,
    MovieVideo, MovieFrame, Rating,
    Review, ReviewLike, Favorite,
    FavoriteItem, History
)

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','user_photo','username','status']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    date_registered = serializers.DateField(format='%d-%%-%Y')
    class Meta:
        model = UserProfile
        fields = ['first_name','last_name','username','email','age',
                  'phone_number','user_photo','status','date_register']


class UserProfileRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name','last_name']


class UserProfileReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username','user_photo']




class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class GenreNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']


class CategoryDetailSerializer(serializers.ModelSerializer):
    genres = GenreNameSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_name', 'genres']


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'genre_name']


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id','country_name']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']


class MovieListSerializer(serializers.ModelSerializer):
    year = serializers.DateField(format='%Y')
    country = CountrySerializer(many=True)
    genre = GenreNameSerializer(many=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'movie_poster', 'movie_name',
            'year', 'country', 'genre', 'movie_status'
        ]



class CountryDetailSerializer(serializers.ModelSerializer):
    country_movies = MovieListSerializer(many=True,read_only=True)
    class Meta:
        model = Country
        fields = ['country_name','country_movies']


class GenreDetailSerializer(serializers.ModelSerializer):
    genre_movies = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = ['genre_name', 'genre_movies']


class DirectorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id','full_name']

class DirectorDetailSerializer(serializers.ModelSerializer):
    birth_date=serializers.DateField(format='%d-%m-%Y')
    director_movies= MovieListSerializer(many=True,read_only=True)
    class Meta:
        model = Director
        fields = ['full_name','director_photo','bio','birth_date','director_movies']


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['full_name']



class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['full_name']



class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id','full_name']

class ActorDetailSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(format='%d-%m-%Y')
    actor_movies = MovieListSerializer(many=True, read_only=True)
    class Meta:
        model = Actor
        fields = ['full_name','actor_photo','bio','birth_date','actor_movies']


class MovieVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieVideo
        fields = ['video_name','video']

class MovieFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieFrame
        fields = ['image']

class RatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%y %H:%M')
    user = UserProfileRatingSerializer
    class Meta:
        model = Rating
        fields = ['user','stars','created_date']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%y %H:%M')
    user = UserProfileReviewSerializer()
    class Meta:
        model = Review
        fields = ['user','comment','parent','created_date']


class MovieDetailSerializer(serializers.ModelSerializer):
    year = serializers.DateField(format='%Y')
    country = CountrySerializer(many=True)
    director = DirectorSerializer(many=True)
    genre = GenreNameSerializer(many=True)
    actor = ActorSerializer(many=True)
    videos = MovieVideoSerializer(many=True, read_only =True)
    frames = MovieFrameSerializer(many=True, read_only =True)
    ratings = RatingSerializer(many=True, read_only =True)
    reviews = ReviewSerializer(many=True, read_only =True)
    get_avg_rating = serializers.SerializerMethodField()
    count_avg_rating = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = ['id','movie_name', 'year', 'country','director','genre',
                 'movie_type','movie_time', 'actor','movie_poster',
                  'trailer','description','movie_status','videos','frames',
                  'get_avg_rating','count_avg_rating', 'ratings', 'reviews']

    def get_avg_rating(self,obg):
            return obg.get_avg_rating()

    def count_avg_rating(self,obg):
            return obg.count_avg_rating()




class ReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewLike
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'



