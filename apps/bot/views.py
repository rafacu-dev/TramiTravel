from datetime import timezone
import requests
import json
from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from apps.bot.models import Pasms


from .bot import *

@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return HttpResponse(True)
    else:
        return HttpResponse(False)
    

@method_decorator(csrf_exempt, name='dispatch')
class PasmsView(View):
    def get(self,request,*args,**kwargs):
        try:
            data = request.GET

            pasms = Pasms.objects.filter(date__isnull=True)

            success = []
            pending = []
            for p in pasms:
                url = f"https://egov.uscis.gov/csol-api/case-statuses/{p.case}"

                response = requests.get(url)
                if response.status_code == 200:
                    json_data = response.json()
                    case = json_data["CaseStatusResponse"]
                    if case["isValid"]:
                        if case["detailsEs"]["actionCodeText"] != "Caso Recibido Y Notificación De Recibo Enviada":
                            p.date = timezone.now()
                            p.save()
                            success.append({"phone":p.phone,"case":p.case,"date":p.date})
                        else:
                            pending.append({"phone":p.phone,"case":p.case})
                    else:
                        p.delete()

            return JsonResponse({"success":success,"pending":pending})
        
        except:
            return HttpResponse("False")
    
    def post(self,request,*args,**kwargs):
        #try:
            data = request.POST

            pasms = Pasms.objects.get_or_create(phone=data["numberPhone"])[1]
            pasms.case = data["numberCase"]
            pasms.save()

            return HttpResponse("True")
        
        #except:
            print("************************************************","Error al crear PASMS")
            return HttpResponse("False")