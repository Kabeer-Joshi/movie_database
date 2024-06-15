from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.movie_list , name='movie_list'),
    path('movies/create/' , views.add_movie, name='add_movie'),
    path('movies/movie-detail/', views.movie_detail , name='movie_detail'),
    path('movies/movie-delete/', views.movie_delete , name='movie_delete'),
    path('movies/review/create-review/',views.create_review , name='create_review'),
    path('movies/review/edit-review/',views.edit_review , name='edit_review'),
    path('movies/review/delete-review/',views.delete_review , name='delete_review'),
    path('movies/watchlist/',views.add_to_watchlist , name='add-to-watchlist'),
    path('movies/watchlist/remove/',views.remove_from_watchlist , name='remove-from-watchlist'),
]