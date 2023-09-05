from django.urls import path
from .views import (AddFlight, Home,BookingView,Flights,GetFligths,
                    Tickets, Message, HomeTraslate,Bookingsagency,EditFlights,Tv,
                    baggagePolicy, download_pdf_ticket, deleteBooking,terminosCondiciones,politicaPrivacidad)

urlpatterns = [
    path('<str:traslate>', HomeTraslate.as_view(),name='index_traslate'),
    path('tv/', Tv.as_view(),name='tv'),
    path('', Home.as_view(),name='index'),
    path('fligth/', Flights.as_view(),name='fligth'),
    path('fligths/get/<str:date_departure>/<str:date_return>/<int:begin>/<int:to>/<int:adults>/<int:children>/<int:infants>/<int:class_type>', GetFligths.as_view(),name='getFligths'),
    path('booking/', BookingView.as_view(),name='booking'),
    path('tickets/', Tickets.as_view(),name='tickets'),
    path('bookings-agency/', Bookingsagency.as_view(),name='bookingsagency'),
    path('tickets/booking-delete/', deleteBooking,name='deleteBooking'),
    path('contact/<str:tag>', Message.as_view(),name='sendMessage'),
    
    path('add-fligth/', AddFlight.as_view(),name='add_flight'),
    path('edit-fligths/<str:flight_ids>/', EditFlights.as_view(),name='edit_flights'),

    path('baggage-policy/<int:bp>', baggagePolicy, name='baggagePolicy'),
    path('download_pdf_ticket/<str:tickets>/<int:option>', download_pdf_ticket,name='download_pdf_ticket'),
    path('terminos-condiciones/', terminosCondiciones, name='terminos_condiciones'),
    path('politica-privacidad/', politicaPrivacidad, name='politica_privacidad'),

]