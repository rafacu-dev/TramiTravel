from django.urls import path
from .views import telegram_webhook,PasmsView,PasmsViewAll

urlpatterns = [
    path('', telegram_webhook, name='telegram_webhook'),
    path('settings-pasms/<int:index>', PasmsView.as_view(), name='Pasms'),
    path('settings-pasms-all/', PasmsViewAll.as_view(), name='PasmsViewAll'),
]