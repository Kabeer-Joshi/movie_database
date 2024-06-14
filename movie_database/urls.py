from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from django.contrib import admin
from django.urls import include , path
from movies.views import registration_view
from movie_database.tokens import CustomTokenObtainPairView

urlpatterns = [

    path('api/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/auth/register/' ,registration_view , name='register'),
    
    path('admin/', admin.site.urls),
    path('api/' , include('movies.urls')),
    
]
