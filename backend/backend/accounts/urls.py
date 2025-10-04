from .views import me, me_profile
from django.urls import path

urlpatterns = [
    path('', me, name='me'),
    path('profile/', me_profile, name='me_profile'),

]