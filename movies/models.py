from django.db import models
from django.contrib.auth.models import User


GENRE_CHOICES = [
    ('romance', 'Romance'),
    ('action', 'Action'),
    ('comedy', 'Comedy'),
    ('drama', 'Drama'),
    ('scifi', 'Science Fiction'),
]

class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    description = models.TextField()
    release_year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE , related_name='reviews')
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='reviewer')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # this is to ensure that a user can only review a movie once
    class Meta:
        unique_together = ('movie', 'user')

    def __str__(self):
        return f'{self.movie.title} - {self.user.username}'
