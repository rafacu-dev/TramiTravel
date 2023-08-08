import time
import requests
from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone

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
    

class PasmsView(View):
    def get(self,request,*args,**kwargs):
        #try:
            data = request.GET

            pasms = Pasms.objects.filter(date__isnull=True)

            success = []
            pending = []
            for p in pasms:
                url = f"https://egov.uscis.gov/csol-api/case-statuses/{p.case}"

                time.sleep(0.01)
                response = requests.get(url, verify=False)
                print("************************************************ GET:",str(p.case),response)
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
        
        #except Exception as error:
            print("************************************************ ERROR en GET:",str(error))
            return HttpResponse("ERROR:" + str(error))
    
    def post(self,request,*args,**kwargs):
        try:
            data = request.POST
            pasms = Pasms.objects.get_or_create(phone=data["numberPhone"])[0]
            pasms.case = data["numberCase"]
            pasms.save()

            return HttpResponse("True")
        
        except Exception as error:
            print("************************************************ ERROR en POST:",str(error))
            return HttpResponse("False")
        


        
class PasmsViewAll(View):
    def get(self,request,*args,**kwargs):
        try:
            data = request.GET

            pasms = Pasms.objects.all()

            success = []
            pending = []
            for p in pasms:
                if p.date == None:
                    pending.append({"phone":p.phone,"case":p.case})
                else:
                    success.append({"phone":p.phone,"case":p.case,"date":p.date})

            return JsonResponse({"success":success,"pending":pending})
        
        except Exception as error:
            print("************************************************ ERROR en GET:",str(error))
            return HttpResponse("False")