from django.shortcuts import render

# Create your views here.
# your_app/views.py
from djoser.views import TokenCreateView
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

# your_app/views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

