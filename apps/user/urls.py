from django.urls import path

from apps.user.views import ChangeInfoAgency

urlpatterns = [
    path('info-agency/', ChangeInfoAgency.as_view(),name='ChangeInfoAgency'),
]
