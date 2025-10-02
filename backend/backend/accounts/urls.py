from .views import me
from django.urls import path

urlpatterns = [
    path('', me, name='me'),
]