from django.contrib import admin

from apps.reservations.models import Airline, Bill, Destinatation, Flight, Charter, Aircraft, Booking, BaggagePolicy

# Register your models here.

class BillAdmin(admin.ModelAdmin):
    model = Bill

admin.site.register(Bill,BillAdmin)
admin.site.register(Destinatation)
admin.site.register(Airline)
admin.site.register(Flight)
admin.site.register(Charter)
admin.site.register(Aircraft)
admin.site.register(Booking)
admin.site.register(BaggagePolicy)
