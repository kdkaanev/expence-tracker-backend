from django.shortcuts import render

# Create your views here.
# your_app/views.py
from djoser.views import TokenCreateView
from django.contrib.auth.models import update_last_login
from rest_framework.response import Response

class CustomTokenCreateView(TokenCreateView):
    def _action(self, serializer):
        response = super()._action(serializer)

        user = serializer.user
        if user:
            update_last_login(None, user)

        return response
