from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.contrib import admin
from django.urls import include , path
from movies.views import registration_view

urlpatterns = [

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/' ,registration_view , name='register'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('admin/', admin.site.urls),
    path('api/' , include('movies.urls')),
    
    
    
]
