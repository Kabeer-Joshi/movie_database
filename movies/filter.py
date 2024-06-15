from .models import Movie
from django_filters import rest_framework as filters

class MovieFilter(filters.FilterSet):
  
  title = filters.CharFilter(lookup_expr='icontains')
  
  class Meta :
    model = Movie
    fields = ['title','genre' , 'release_year']