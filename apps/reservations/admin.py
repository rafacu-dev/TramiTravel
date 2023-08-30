from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from apps.reservations.models import Airline, Bill, Destinatation, Flight, Charter, Aircraft, Booking, BaggagePolicy, ClassType, TvImages

# Register your models here.

class BillAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Bill._meta.fields]
    search_fields = ["id","code","zelle","zelle_owner"]
    list_filter = ["paid",]
    model = Bill
    
class DestinatationAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Destinatation._meta.fields]
    search_fields = ["id","city","country","cityCode","countryCode"]
    list_filter = ["city","country"]
    model = Destinatation
    
class AirlineAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Airline._meta.fields]
    search_fields = ["id","name","nameCode"]
    list_filter = ["actived",]
    model = Airline
    
    
def edit_flights(modeladmin, request, queryset):
    flight_ids = '-'.join(str(flight.id) for flight in queryset)
    url = reverse('edit_flights', args=[flight_ids])
    return redirect(url)

edit_flights.short_description = "Editar vuelos seleccionados"

class FlightAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Flight._meta.fields]
    search_fields = ["id","gate","number"]

    list_filter = ["begin","to","gate","charter","aircraft","class_type","actived"]
    date_hierarchy = "date"
    actions = [edit_flights]
    model = Flight
    
class CharterAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Charter._meta.fields]
    search_fields = ["id","name"]
    list_filter = ["name","actived"]
    model = Charter
    
class AircraftAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Aircraft._meta.fields]
    search_fields = ["id","model"]
    list_filter = ["model","first_class_seats","actived"]
    model = Aircraft
    
class BookingAdmin(admin.ModelAdmin):
    list_display=[field.name for field in Booking._meta.fields]
    search_fields = ["id","firstName","middleName",
                     "lastName","motherLastName",
                     "birth","gender","email","phone",
                     "documentNumber","documentExpiration",
                     "documentType","documentCountry",
                     "secondaryDocumentNumber",
                     "secondaryDocumentExpiration",
                     "secondaryDocumentType","secondaryDocumentCountry",
                     "streetBegin","cityBegin","stateBegin",
                     "streetTo","cityTo","stateTo",
                     "reservationCode","pnr"]
    list_filter = ["user","license","actived"]
    date_hierarchy = "date"
    model = Booking
    
class BaggagePolicyAdmin(admin.ModelAdmin):
    list_display=[field.name for field in BaggagePolicy._meta.fields]
    search_fields = ["id","identifier"]
    list_filter = ["actived",]
    model = BaggagePolicy
    
class ClassTypeAdmin(admin.ModelAdmin):
    list_display=[field.name for field in ClassType._meta.fields]
    search_fields = list_display
    list_filter = ["actived",]
    model = ClassType

admin.site.register(Bill,BillAdmin)
admin.site.register(Destinatation,DestinatationAdmin)
admin.site.register(Airline,AirlineAdmin)
admin.site.register(Flight,FlightAdmin)
admin.site.register(Charter,CharterAdmin)
admin.site.register(Aircraft,AircraftAdmin)
admin.site.register(Booking,BookingAdmin)
admin.site.register(BaggagePolicy,BaggagePolicyAdmin)
admin.site.register(ClassType,ClassTypeAdmin)
admin.site.register(TvImages)