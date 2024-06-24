from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Movie, Review, Watchlist
from django.urls import reverse

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        self.regular_user = User.objects.create_user('regular', 'regular@example.com', 'regularpass')
        self.movie = Movie.objects.create(
            title='Test Movie',
            genre='action',
            description='Test description',
            release_year=2023
        )

    def test_movie_list(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_add_movie(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'title': 'New Movie',
            'genre': 'comedy',
            'description': 'New description',
            'release_year': 2024
        }
        response = self.client.post(reverse('add_movie'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_movie_detail(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(reverse('movie_detail'), {'id': self.movie.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Movie')

    def test_movie_delete(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(reverse('movie_delete'), {'id': self.movie.id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_review(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'movieId': self.movie.id,
            'rating': 8,
            'comment': 'Great movie!'
        }
        response = self.client.post(reverse('create_review'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_review(self):
        self.client.force_authenticate(user=self.regular_user)
        review = Review.objects.create(movie=self.movie, user=self.regular_user, rating=7, comment='Good movie')
        data = {
            'reviewId': review.id,
            'rating': 9,
            'comment': 'Actually, it was great!'
        }
        response = self.client.post(reverse('edit_review'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_review(self):
        self.client.force_authenticate(user=self.regular_user)
        review = Review.objects.create(movie=self.movie, user=self.regular_user, rating=7, comment='Good movie')
        response = self.client.post(reverse('delete_review'), {'reviewId': review.id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_add_to_watchlist(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(reverse('add-to-watchlist'), {'movieId': self.movie.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_remove_from_watchlist(self):
        self.client.force_authenticate(user=self.regular_user)
        Watchlist.objects.create(user=self.regular_user, movie=self.movie)
        response = self.client.post(reverse('remove-from-watchlist'), {'movieId': self.movie.id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)