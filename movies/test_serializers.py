from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from .models import Movie, Review, Watchlist
from .serializers import (
    RegistrationSerializer,
    UserSerializer,
    ReviewSerializer,
    MovieSerializer,
    WatchlistSerializer
)

class RegistrationSerializerTestCase(TestCase):
    def test_registration_serializer(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        }
        serializer = RegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')

    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user)
        self.assertEqual(serializer.data['username'], 'testuser')
        self.assertEqual(serializer.data['email'], 'test@example.com')

class ReviewSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.movie = Movie.objects.create(title='Test Movie', genre='action', description='Test description', release_year=2023)
        self.review = Review.objects.create(movie=self.movie, user=self.user, rating=8, comment='Great movie!')

    def test_review_serializer(self):
        serializer = ReviewSerializer(instance=self.review)
        self.assertEqual(serializer.data['rating'], 8)
        self.assertEqual(serializer.data['comment'], 'Great movie!')

class MovieSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.movie = Movie.objects.create(title='Test Movie', genre='action', description='Test description', release_year=2023)
        self.review = Review.objects.create(movie=self.movie, user=self.user, rating=8, comment='Great movie!')

    def test_movie_serializer(self):
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = self.user
        serializer = MovieSerializer(instance=self.movie, context={'request': request})
        self.assertEqual(serializer.data['title'], 'Test Movie')
        self.assertEqual(serializer.data['genre'], 'action')

class WatchlistSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.movie = Movie.objects.create(title='Test Movie', genre='action', description='Test description', release_year=2023)
        self.watchlist = Watchlist.objects.create(user=self.user, movie=self.movie)

    def test_watchlist_serializer(self):
        serializer = WatchlistSerializer(instance=self.watchlist)
        self.assertEqual(serializer.data['user'], self.user.id)
        self.assertEqual(serializer.data['movie'], self.movie.id)