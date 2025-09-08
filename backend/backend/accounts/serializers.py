from djoser.serializers import UserCreateSerializer, UserSerializer,TokenCreateSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from .models import ExpenceTrackerUser




# your_app/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django.contrib.auth.models import update_last_login

# your_app/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)


        # self.user е достъпен тук
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        update_last_login(None, self.user)

        return data

