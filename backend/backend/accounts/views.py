from django.shortcuts import render


from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, ProfileSerializer
from rest_framework import status


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
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

            
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def me_profile (request):
    profile = request.user.profile
    if request.method == 'GET':
        return Response(ProfileSerializer(profile).data)
    if request.method == 'PATCH':
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return  Response(serializer.errors, status=400)
        
