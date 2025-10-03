from djoser.serializers import UserCreateSerializer, UserSerializer,TokenCreateSerializer
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from .models import ExpenceTrackerUser, Profile


# your_app/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django.contrib.auth.models import update_last_login

# your_app/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login

ExpenceTrackerUser = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)


        # self.user е достъпен тук
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        update_last_login(None, self.user)

        return data



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name',)


class ExpenceTrackerUserSerializer(UserSerializer):
    profile = ProfileSerializer(required=False)

    class Meta(UserSerializer.Meta):
        model = ExpenceTrackerUser
        fields = ('id', 'email', 'profile',)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = super().update(instance, validated_data)

        if profile_data:
            profile = getattr(user, 'profile', None)
            if profile:
               for atr, value in profile_data.items():
                   setattr(profile, attr, value)
                   profile.save()
            else:
                Profile.objects.create(user=user, **profile_data)

        user.refresh_from_db()

        return user



