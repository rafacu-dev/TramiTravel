from django.urls import path
from .views import telegram_webhook,search_link

urlpatterns = [
    path('', telegram_webhook, name='telegram_webhook'),
    path('search-link/add/', search_link, name='search_link'),
]