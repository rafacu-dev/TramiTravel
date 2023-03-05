import threading

from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages

from core.languages import get_strings
from apps.bot.bot import send_message_to_channel

from .models import Menu, Seccion

# Create your views here.

class Service(View):
    def get(self,request,tag,*args,**kwargs):

        menus = Menu.objects.all().order_by('position')        
        seccion = Seccion.objects.get(tag=tag)        
        strings,language = get_strings(request.COOKIES)
        context = {
            "language":language,
            "strings" : strings,
            "seccion":seccion,
            "menus" :menus
            }

        return render(request,'service.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        
        message = f"<u>⚠️Un cliente desea contactar con la agencia:\n\n</u>"
        message += f"Nombre:  <b><code>{data['name']}</code></b>,\n"
        message += f"Email:  <b><code>{data['email']}</code></b>,\n"
        message += f"Phone:  <b><code>{data['phone']}</code></b>"

        if data["menssage"] != "":
            message += f",\nMensaje:  <b>{data['menssage']}</b>"

        
        t = threading.Thread(target=lambda:send_message_to_channel(message))
        t.start()
        
        messages.success(request, 'Nuestro personal se comunicará con usted en un momento. Gracias por contactarnos.')
        menus = Menu.objects.all().order_by('position')
        
        seccion = Seccion.objects.get(tag=request.path.split("/")[2])
        
        strings,language = get_strings(request.COOKIES)
        context = {
            "language":language,
            "strings" : strings,
            "seccion":seccion,
            "menus" :menus
            }

        return render(request,'service.html',context)


class Services(View):
    def get(self,request,tag,*args,**kwargs):

        menus = Menu.objects.all().order_by('position')        
        seccions = Menu.objects.get(tag=tag)
        
        strings,language = get_strings(request.COOKIES)
        context = {
            "language":language,
            "strings" : strings,
            "seccions":seccions,
            "menus" :menus
            }

        return render(request,'services.html',context)
        
class Contact(View):
    def get(self,request,*args,**kwargs):

        menus = Menu.objects.all().order_by('position')
        
        strings,language = get_strings(request.COOKIES)
        context = {
            "language":language,
            "strings" : strings,
            "menus" :menus
            }

        return render(request,'contact.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        
        message = f"<u>⚠️Un cliente desea contactar con la agencia:\n\n</u>"
        message += f"Nombre:  <b><code>{data['name']}</code></b>,\n"
        message += f"Email:  <b><code>{data['email']}</code></b>,\n"
        message += f"Phone:  <b><code>{data['phone']}</code></b>"

        if data["menssage"] != "":
            message += f",\nMensaje:  <b>{data['menssage']}</b>"
        
        t = threading.Thread(target=lambda:send_message_to_channel(message))
        t.start()
        
        strings,language = get_strings(request.COOKIES)
        
        messages.success(request, strings["succesMessage"])
        menus = Menu.objects.all().order_by('position')


        context = {
            "language":language,
            "strings" : strings,
            "menus" :menus
            }

        return render(request,'contact.html',context)
      