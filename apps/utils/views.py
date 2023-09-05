
from datetime import datetime
import json
import threading
from django.utils import timezone
from django.shortcuts import HttpResponse, redirect, render
from django.views.generic import View
from django.utils.decorators import method_decorator
from apps.bot.bot import send_message_confirm_payment
from apps.menus.models import Menu
from apps.utils.models import Payment
from apps.utils.utils import permission_checked
from core.languages import get_strings

from apps.utils import countries_states_cities


@method_decorator(permission_checked, name='dispatch')
class Pay(View):    
    def get(self,request,*args,**kwargs):

        data = request.GET

        menus = Menu.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)

        payments = Payment.objects.filter(user = request.user)
        

        context = {
            "language":language,
            "strings" : strings,
            "menus" :menus,
            "payments":payments,
            "product":data["product"],
            "code":datetime.now().microsecond,
            "ammount":data["ammount"]
            }

        return render(request,'payment.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        dataGet = request.GET

        menus = Menu.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)
        
        zelle_owner = data["zelle-owner"]
        p = Payment.objects.create(
                                zelle_owner=zelle_owner,
                               user=request.user,
                               product=dataGet["product"],
                               code=data["code"],
                               ammount=dataGet["ammount"]
                            )
        
        emailPayment = data["emailPayment"]
        phonePayment = data["phonePayment"]
        if emailPayment != "":
            p.zelle = emailPayment
        else:
            p.zelle = phonePayment
        p.save()

        payments = Payment.objects.filter(user = request.user)
        
        message = f"<b>COMPROBACION DE PAGO DE PAQUETE CON BILL-{p.id}:</b>\n\n"
        message += f"<b>Usuario:</b> <code>{request.user}</code>\n"
        message += f"<b>Zelle:</b> <code>{p.zelle}</code>\n"
        message += f"<b>Codigo:</b> <code>{p.code}</code>\n\n"
        message += f"<b>Monto requerido:</b> <code>{p.ammount}</code>\n"   
        
        t = threading.Thread(target=lambda:send_message_confirm_payment(message,id))
        t.start()

        context = {
            "language":language,
            "strings" : strings,
            "menus" :menus,
            "payments":payments,
            "product":dataGet["product"],
            "code":data["code"],
            "ammount":dataGet["ammount"],
            "success":True
            }

        return render(request,'payment.html',context)



#https://github.com/dr5hn/countries-states-cities-database
def getStatesView(request,name):
    names = []    
    for item in countries_states_cities.countries_list:
        if 'name' in item and item['name'] == name:
            for state in item["states"]:
                if 'name' in state:names.append(state['name'])
            break
    data_return =json.dumps({"names":names})
    return HttpResponse(data_return,"application/json")


def getCitiesView(request,cuntry,state_name):
    names = []
    for item in countries_states_cities.countries_list:
        if 'name' in item and item['name'] == cuntry:
            for state in item["states"]:
                if state_name == state["name"] and 'cities' in state:
                    for citie in state["cities"]:
                        if 'name' in citie:names.append(citie['name'])
                    break
            break
    data_return =json.dumps({"names":names})
    return HttpResponse(data_return,"application/json")