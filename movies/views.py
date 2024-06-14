from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view ,permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Movie
from .serializers import MovieSerializer , RegistrationSerializer , ReviewSerializer


@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email

            refresh = RefreshToken.for_user(account)
            data['token'] = {
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                            }
       
        else:
            data = serializer.errors
        
        return Response(data, status=status.HTTP_201_CREATED)


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

@api_view(['POST'  , 'PUT'])
def movie_detail(request):
    movieId = request.data.get('id')
    try:
        movie = Movie.objects.get(pk=movieId)
        
        if request.method == 'POST':
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = MovieSerializer(movie , data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def movie_delete(request):
    movieId = request.data.get('id')
    try:
        movie = Movie.objects.get(pk=movieId)
        movie.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
    
# REVIEWS 

@api_view(['POST'])
def create_review(request):
    movieId = request.data.get('movieId')
    try:
        movie = Movie.objects.get(id=movieId)
        print("i got movie as " , movie)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ReviewSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    