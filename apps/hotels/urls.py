from django.urls import path

from apps.hotels.views import Hotels,BookingView,ReservationsView,ReservationsAgencieView

urlpatterns = [
    path('reservations/', ReservationsView.as_view(),name='reservations'),
    path('reservations-agencie/', ReservationsAgencieView.as_view(),name='reservationsAgencie'),
    path('hotels/', Hotels.as_view(),name='hotels'),
    path('booking-package/', BookingView.as_view(),name='booking-package'),
]