from django.shortcuts import render


from djoser.views import TokenCreateView
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([])
def me(request):
    user = request.user
    profile = getattr(user, 'profile', None)

    return Response({
        'id': user.id,
        'email': user.email,
        'profile': {
            'first_name': getattr(profile, 'first_name', '') if profile else '',
            'last_name': getattr(profile, 'last_name', '') if profile else '',
        }
    })