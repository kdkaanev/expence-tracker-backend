from djoser.serializers import UserCreateSerializer, UserSerializer

from .models import ExpenceTrackerUser


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = ExpenceTrackerUser
        fields = ('id', 'email', 'password',)

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = ExpenceTrackerUser
        fields = ('id', 'email',)