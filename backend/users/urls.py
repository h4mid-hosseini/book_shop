from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('create-sample-users/', views.CreateSampleUsers.as_view(), name='create_sample_users')
]
