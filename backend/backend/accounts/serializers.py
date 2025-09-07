from djoser.serializers import UserCreateSerializer, UserSerializer,TokenCreateSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from .models import ExpenceTrackerUser




# your_app/serializers.py
from djoser.serializers import TokenCreateSerializer
from django.contrib.auth.models import update_last_login

class CustomTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user  # Djoser вече сетва self.user при успешен login
        print("DEBUG: CustomTokenCreateSerializer called for", user)
        if user:
            update_last_login(None, user)

        return data
