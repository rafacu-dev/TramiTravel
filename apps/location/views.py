from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apps.location.models import Location

# Create your views here.

@csrf_exempt
def location(request,set):
    if request.method == 'POST':
        data = request.POST
        latitude = data['latitude']
        longitude = data['longitude']
        androidId = data['androidId'][1:-1]
        location = Location.objects.create(
            latitude=latitude,
            longitude=longitude,
            androidId=androidId
        )
        location.save()
        return HttpResponse("ok")
    
    elif request.method == 'GET':
        return HttpResponse("ok")