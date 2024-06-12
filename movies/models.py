from django.db import models

# Create your models here.

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
    release_year = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
