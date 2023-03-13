from django.urls import path
from .views import (Home,BookingView,Flights,GetFligths,
                    Tickets, Message, HomeTraslate,
                    baggagePolicy, download_pdf_ticket, deleteBooking)

urlpatterns = [
    path('<str:traslate>', HomeTraslate.as_view(),name='index_traslate'),
    path('', Home.as_view(),name='index'),
    path('fligth/', Flights.as_view(),name='fligth'),
    path('fligths/get/<str:date_departure>/<str:date_return>/<int:begin>/<int:to>/<int:adults>/<int:children>/<int:infants>', GetFligths.as_view(),name='getFligths'),
    path('booking/', BookingView.as_view(),name='booking'),
    path('tickets/', Tickets.as_view(),name='tickets'),
    path('tickets/booking-delete/', deleteBooking,name='deleteBooking'),
    path('contact/<str:tag>', Message.as_view(),name='sendMessage'),
    path('baggage-policy/<int:bp>', baggagePolicy, name='baggagePolicy'),
    path('download_pdf_ticket/<str:tickets>/<int:option>', download_pdf_ticket,name='download_pdf_ticket'),
]