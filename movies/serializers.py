from rest_framework import serializers
from .models import Movie , Review
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' , 'username']
        
class ReviewSerializer(serializers.ModelSerializer):
    
    reviewer = serializers.StringRelatedField(source="user.username" , read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        
        

class MovieSerializer(serializers.ModelSerializer):
    
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = '__all__'