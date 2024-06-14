from rest_framework import status
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.permissions import IsAuthenticated , AllowAny , IsAdminUser
from rest_framework.response import Response
from .models import Movie , Review
from .serializers import MovieSerializer , RegistrationSerializer , ReviewSerializer
from movie_database.tokens import CustomRefreshToken


@api_view(['POST',])
@permission_classes((AllowAny,))
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email

            refresh = CustomRefreshToken.for_user(account)  # use the custom token class
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
    print("Is this user a staff member? ", request.user.is_staff)
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
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
            if not request.user.is_staff:
                return Response({'message': 'You are not allowed to edit this movie'}, status=403)
            serializer = MovieSerializer(movie , data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdminUser])  
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
    # Get the movie
    try:
        movie_id = request.data.get('movieId')
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=404)

    # Get the user from the request
    user = request.user
    
    # Check if the user has already reviewed this movie
    if Review.objects.filter(movie=movie, user=user).exists():
        return Response({'message': 'You have already reviewed this movie'}, status=400)

    # Create a new review
    review = Review(movie=movie, user=user)

    # Serialize the data
    serializer = ReviewSerializer(review, data=request.data)

    # Validate and save the data
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)
    
    
@api_view(['POST'])
def edit_review(request):
    reviewId = request.data.get('reviewId')
    try:
        review = Review.objects.get(pk=reviewId)
        if review.user != request.user:
            return Response({'message': 'You are not allowed to edit this review'}, status=403) 
        serializer = ReviewSerializer(review , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['POST'])
def delete_review(request):
    reviewId = request.data.get('reviewId')
    try:
        review = Review.objects.get(pk=reviewId)
        if review.user != request.user:
            return Response({'message': 'You are not allowed to delete this review'}, status=403)
        review.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    