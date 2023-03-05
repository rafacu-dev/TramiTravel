from django.urls import path
from .views import Refills

urlpatterns = [
    path('', Refills.as_view(),name="refills"),
]
