from django.views.generic import View
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt


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

@csrf_exempt
def search_link(request):
    try:
        data = request.POST
        msg = ""
        for k in  data.keys():
             msg += k + ": <b><code>" + data[k] + "</code></b>\n"
        send_message_to_searchl_link(msg)
        return HttpResponse("True")
    except:
        return HttpResponse("False")