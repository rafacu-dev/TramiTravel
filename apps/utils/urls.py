from django.urls import path
from .views import (Pay)

urlpatterns = [
    path('pay/', Pay.as_view(),name='Pay'),
]