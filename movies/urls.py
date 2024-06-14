from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.movie_list , name='movie_list'),
    path('movies/create/' , views.add_movie, name='add_movie'),
    path('movies/movie-detail/', views.movie_detail , name='movie_detail'),
    path('movies/movie-delete/', views.movie_delete , name='movie_delete')
]