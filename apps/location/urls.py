from django.urls import path
from .views import location

urlpatterns = [
    path('send-location/<str:set>', location,name='location'),
]