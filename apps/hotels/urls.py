from django.urls import path

from apps.hotels.views import Hotels,BookingView,ReservationsView,ReservationsagencyView

urlpatterns = [
    path('reservations/', ReservationsView.as_view(),name='reservations'),
    path('reservations-agency/', ReservationsagencyView.as_view(),name='reservationsagency'),
    path('hotels/', Hotels.as_view(),name='hotels'),
    path('booking-package/', BookingView.as_view(),name='booking-package'),
]