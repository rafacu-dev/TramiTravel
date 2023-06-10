
from django.shortcuts import HttpResponse, redirect, render
from django.views.generic import View
from apps.menus.models import Menu

from apps.refills.models import Config, Refill
from ..bot.bot import *
from random import randint as ri

class Refills(View):
    def get(self,request,*args,**kwargs):
        #if not request.user.is_authenticated: return  redirect("index")
        
        code = f"{ri(0,9)}{ri(0,9)}{ri(0,9)}{ri(0,9)}{ri(0,9)}"

        try:porcent = float(Config.objects.get(clave = "porcentRefills"))
        except:porcent = 0.25

        refills = Refill.objects.all().reverse()

        menus = Menu.objects.all().order_by('position')
        
        context = {
            "porcent" : porcent,
            "code" : code,
            "refills" : refills,
            "menus" :menus
            }

        return render(request,'refills.html',context)

    def post(self,request,*args,**kwargs):
        if not request.user.is_authenticated: return  redirect("index")
        data = request.POST
        try:porcent = float(Config.objects.get(clave = "porcentRefills"))
        except:porcent = 0.25
        razon = 100/(100 + (100 * porcent))
        try:
            deposit = float(data["quantity-deposit"])
            code = data["code"]
            emailZelle = data["emailPayment"]
            userZelle = data["userPayment"]
            deposit = deposit
            receiver = deposit * razon
            card = data["MLC-card"]
            receivingPerson = data["receiving-person"]
            
            Refill.objects.create(
                user = request.user,
                code = code,
                emailZelle = emailZelle,
                userZelle = userZelle,
                deposit = deposit,
                receiver = receiver,
                card = card,
                receivingPerson = receivingPerson
            )

            message = f"El usuario {request.user} indicó que realizo una recarga de <b>{deposit} USD a entregar {receiver} MLC</b>, "
            message += f"en la tarjeta <b>{card}</b> a nombre de <b>{receivingPerson}</b>, "
            message += "y proporcionó los siguientes datos de <b>Zelle</b>: \n" 
            message += f"<b>Usuario:</b> {userZelle}\n"
            message += f"<b>Email/Phone:</b> {emailZelle}\n"
            message += f"<b>Codigo</b> {code}"
            
            t = threading.Thread(target=lambda:send_message_to_channel(message))
            t.start()
            
            return  redirect("refills")

        except: return  redirect("refills")
