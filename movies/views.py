from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Movie
from .serializers import MovieSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_movie(request):
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'  , 'PUT', 'DELETE'])
def movie_detail(request):
    movieId = request.data.get('id')
    try:
        movie = Movie.objects.get(pk=movieId)
        
        if request.method == 'GET':
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = MovieSerializer(movie , data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            movie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    