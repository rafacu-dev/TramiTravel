from django.contrib import admin
from apps.location.models import Location,GetRequests

admin.site.register(Location)



class GetRequestsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GetRequests._meta.fields]
    model = GetRequests

admin.site.register(GetRequests,GetRequestsAdmin)