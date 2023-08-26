import json
import os
import threading, re
from django.http import FileResponse, JsonResponse

from django.views.decorators.cache import never_cache

from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from apps.utils.countries import getCountries
from apps.utils.utils import permission_checked
from core import settings



from core.languages import get_strings
from apps.bot.bot import send_message_to_channel

from .models import Menu, Seccion

# Create your views here.

@method_decorator(permission_checked, name='dispatch')
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

@method_decorator(permission_checked, name='dispatch')
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
     
@method_decorator(permission_checked, name='dispatch')   
class Contact(View):
    def get(self,request,*args,**kwargs):
        menus = Menu.objects.filter(actived=True).order_by('position')        
        strings,language = get_strings(request.COOKIES)
        context = {
            "language":language,
            "strings" : strings,
            "menus" :menus
            }

        return render(request,'contact.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        
        strings,language = get_strings(request.COOKIES)
        
        messages.success(request, strings["succesMessage"])
        menus = Menu.objects.all().order_by('position')

        context = {
            "language":language,
            "strings" : strings,
            "menus" :menus
            }

        # Validar que no haya enlaces
        if re.search("(http|https)://[^\s]+", data['menssage']):return render(request,'contact.html',context)

        # Validar que no haya direcciones de correo
        if re.search("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", data['menssage']):return render(request,'contact.html',context)

        # Validar que solo hay caracteres en inglés
        if re.search("[^a-zA-Z\s.,?!]+", data['menssage']):return render(request,'contact.html',context)
        
        message = f"<u>⚠️Un cliente desea contactar con la agencia:\n\n</u>"
        message += f"Nombre:  <b><code>{data['name']}</code></b>,\n"
        message += f"Email:  <b><code>{data['email_contact']}</code></b>,\n"
        message += f"Phone:  <b><code>{data['phone']}</code></b>"

        if data["menssage"] != "":
            message += f",\nMensaje:  <b>{data['menssage']}</b>"
        
        t = threading.Thread(target=lambda:send_message_to_channel(message))
        t.start()

        return render(request,'contact.html',context)
      

def download_apk(request):
    apk_file_path = os.path.join(settings.BASE_DIR, 'static/app/TramiTravel.apk')
    return FileResponse(open(apk_file_path, 'rb'), as_attachment=True)


#https://github.com/dr5hn/countries-states-cities-database
@never_cache
def getCountriesView(request):
    with open('apps/menus/countries-states-cities.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    names = []
    
    for item in data:
        if 'name' in item:
            name = item['name']
            names.append(name)
    return JsonResponse(names, safe=False)

@never_cache
def getStatesView(request):
    name = request.GET["name"]
    with open('apps/menus/countries-states-cities.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    names = []
    
    for item in data:
        if 'name' in item and item['name'] == name:
            for state in item["states"]:
                if 'name' in state:names.append(state['name'])
            break
    return JsonResponse(names, safe=False)

@never_cache
def getCitiesView(request):
    cuntry = request.GET["cuntry"]
    state_name = request.GET["state"]  
    with open('apps/menus/countries-states-cities.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    names = []
    for item in data:
        if 'name' in item and item['name'] == cuntry:
            for state in item["states"]:
                if state_name == state["name"] and 'cities' in state:
                    for citie in state["cities"]:
                        if 'name' in citie:names.append(citie['name'])
                    break
            break
    return JsonResponse(names, safe=False)


class Form(View):
    def get(self,request,form_name,*args,**kwargs):
        context = {}
        return render(request,f'forms/{form_name}.html',context)
    
    def post(self,request,*args,**kwargs):
        data = request.POST 
        print(data)
        
        
        t = threading.Thread(target=lambda:send_message_to_channel(str(data)))
        t.start()

        return redirect("index")