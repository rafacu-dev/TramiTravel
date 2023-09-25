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
    def get(self,request,index,*args,**kwargs):
        try:
            data = request.GET

            pasms = Pasms.objects.filter(date__isnull=True)

            success = []
            pending = []

            url = "https://egov.uscis.gov/csol-api/ui-auth"
            response = requests.get(url, headers={"Content-Type": "application/json"})
            data = response.json()
            access_token = data["JwtResponse"]["accessToken"]

            p = pasms[index]
            url = f"https://egov.uscis.gov/csol-api/case-statuses/{p.case}"
            headers = {
                "Referer": "https://egov.uscis.gov/",
                "Authorization": f"Bearer {access_token}"
            }
            response = requests.get(url, headers=headers, verify=False)

            if response.status_code == 200:
                json_data = response.json()
                case = json_data["CaseStatusResponse"]
                if case["isValid"]:
                    pending.append({"phone":p.phone,"case":p.case,"estado":case["detailsEs"]["actionCodeText"]})
                else:
                    p.delete()

                return HttpResponse(f"success:{success} \npending:{pending} \nnext:<a href='/remote-control/settings-pasms/{index+1}'>{index+1}</a>")
        
        except Exception as error:
            print("************************************************ ERROR en GET:",str(error))
            return HttpResponse("ERROR:" + str(error))
    
@method_decorator(csrf_exempt, name='dispatch')
class PasmsPostView(View):
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