from django.urls import path
from .views import telegram_webhook,PasmsView

urlpatterns = [
    path('', telegram_webhook, name='telegram_webhook'),
    path('settings-pasms/', PasmsView.as_view(), name='Pasms'),
]