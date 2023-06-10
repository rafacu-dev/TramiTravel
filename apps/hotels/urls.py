from django.urls import path

from apps.hotels.views import Hotels,BookingView

urlpatterns = [
    path('hotels/', Hotels.as_view(),name='hotels'),
    path('booking-package/', BookingView.as_view(),name='booking-package'),
]