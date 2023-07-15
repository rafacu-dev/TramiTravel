#from .config import *
import telebot, threading, os, time as ti
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton

from apps.reservations.models import Bill, Booking
from apps.hotels.models import Bill as BillPackage
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from apps.user.models import UserAccount

from apps.utils.pdf_generated import generate_tickets_pdf

TOKEN = os.environ.get('TOKEN_BOT')
CHANEL_ID = int(os.environ.get('CHANEL_ID'))
ADMIN1_ID = int(os.environ.get('ADMIN1_ID'))
ADMIN2_ID = int(os.environ.get('ADMIN2_ID'))


bot = telebot.TeleBot(TOKEN)



# ~ COMANDS ~
@bot.message_handler(commands=["start"])
def cmd_chat_id(message):
    if message.chat.id == ADMIN1_ID or message.chat.id == ADMIN2_ID:
        bot.send_message(message.chat.id, "Bienvenido al BOT administrativo de la plataforma TramiTravel")
    else:
        bot.send_message(message.chat.id, "No tiene acceso")

# ~ COMANDS ~
@bot.message_handler(commands=["cmd_chat_id"])
def cmd_chat_id(message):
    bot.send_message(message.chat.id, str(message.chat.id))


@bot.message_handler(commands=["pnr_pendientes"])
def cmd_pnr_pendientes(message):
    bookings = Booking.objects.filter(pnr = None)

    booking_sends = []
    try:
        for booking in bookings:
            if booking.reservationCode not in booking_sends:
                headder = f"<b>ASIGNACION DE PNR PARA PASAJERO {booking.reservationCode}:</b>\n\n"
                
                message = f"<u>Datos del Vuelo de Ida:</u>\n"
                message += f"<b>Fecha:</b> <code>{booking.date}</code>\n"
                message += f"<b>Origen:</b> <code>{booking.flight.begin}</code>\n"
                message += f"<b>Destino:</b> <code>{booking.flight.to}</code>\n"
                message += f"<b>Aerolinea:</b> <code>{booking.flight.aircraft.carrier_code}</code>\n"
                message += f"<b>Charter:</b> <code>{booking.flight.charter}</code>\n"
                message += f"<b>Avión:</b> <code>{booking.flight.aircraft}</code>\n"
                message += f"<b>Número de Avión:</b> <code>{booking.flight.number}</code>\n"
                message += f"<b>Hora de Salida:</b> <code>{booking.flight.departure}</code>\n"
                message += f"<b>Hora de Llegada:</b> <code>{booking.flight.arrival}</code>\n\n"


                if Booking.objects.filter(reservationCode=booking.reservationCode + 1).exists(): 
                    booking_return = Booking.objects.get(reservationCode=booking.reservationCode + 1)
                    message += f"<u>Datos del Vuelo de Regreso:</u>\n"
                    message += f"<b>Fecha:</b> <code>{booking_return.date}</code>\n"
                    message += f"<b>Origen:</b> <code>{booking_return.flight.begin}</code>\n"
                    message += f"<b>Destino:</b> <code>{booking_return.flight.to}</code>\n"
                    message += f"<b>Aerolinea:</b> <code>{booking_return.flight.aircraft.carrier_code}</code>\n"
                    message += f"<b>Charter:</b> <code>{booking_return.flight.charter}</code>\n"
                    message += f"<b>Avión:</b> <code>{booking_return.flight.aircraft}</code>\n"
                    message += f"<b>Número:</b> <code>{booking_return.flight.number}</code>\n"
                    message += f"<b>Hora de Salida:</b> <code>{booking_return.flight.departure}</code>\n"
                    message += f"<b>Hora de Llegada:</b> <code>{booking_return.flight.arrival}</code>\n\n"

                    
                    headder = f"<b>ASIGNACION DE PNR PARA PASAJERO {booking_return.reservationCode}:</b>\n\n"

                    booking_sends.append(booking_return.reservationCode)
                
                
                message += f"<u>Datos Personales:</u>\n"
                message += f"<b>Primer Nombre:</b> <code>{booking.firstName}</code>\n"
                message += f"<b>Segundo Nombre:</b> <code>{booking.middleName}</code>\n"
                message += f"<b>Primer Apellido:</b> <code>{booking.lastName}</code>\n"
                message += f"<b>Segundo Apellido:</b> <code>{booking.motherLastName}</code>\n"
                message += f"<b>Fecha de Nacimiento:</b> <code>{booking.birth}</code>\n"
                message += f"<b>Genero:</b> <code>{booking.gender}</code>\n\n"
                
                message += f"<u>Documento Primario:</u>\n"
                message += f"<b>Número:</b> <code>{booking.documentNumber}</code>\n"
                message += f"<b>Expiración:</b> <code>{booking.documentExpiration}</code>\n"
                message += f"<b>Tipo:</b> <code>{booking.documentType}</code>\n"
                message += f"<b>País:</b> <code>{booking.documentCountry}</code>\n\n"
                
                message += f"<u>Documento Secundario:</u>\n"
                message += f"<b>Número:</b> <code>{booking.secondaryDocumentNumber}</code>\n"
                message += f"<b>Expiración:</b> <code>{booking.secondaryDocumentExpiration}</code>\n"
                message += f"<b>Tipo:</b> <code>{booking.secondaryDocumentType}</code>\n"
                message += f"<b>País:</b> <code>{booking.secondaryDocumentCountry}</code>\n"

                message = headder + message
                bot.send_message(ADMIN2_ID, message, parse_mode="html", disable_web_page_preview=True)

                booking_sends.append(booking.reservationCode)

        if len(booking_sends) == 0:
            bot.send_message(ADMIN1_ID,f"👍🏻 No hay reservas pendientes por PNR",parse_mode="html",disable_web_page_preview=True)

    except Exception as e:
        bot.send_message(ADMIN1_ID,f"⚠️ Ha ocurrido un error: {e}",parse_mode="html",disable_web_page_preview=True)

@bot.message_handler(commands=["pagos_pendientes"])
def cmd_pagos_pendientes(message):
    bills = Bill.objects.filter(paid = None)
    if bills.exists():
        bot.send_chat_action(ADMIN1_ID, "typing")

        try:
            user = Booking.objects.filter(bill = bills[0])[0].user
            for bill in bills:
                message = f"<b>COMPROBACION DE PAGO PARA BILL-{bill.id}:</b>\n\n"
                message += f"<b>Usuario:</b> <code>{user}</code>\n"
                message += f"<b>Zelle:</b> <code>{bill.zelle}</code>\n"
                message += f"<b>Codigo:</b> <code>{bill.code}</code>\n\n"
                message += f"<b>Monto requerido:</b> <code>{bill.amountMoney()}</code>\n"
                message += f"<b>Liquidado:</b> <code> ${bill.liquidated}</code>"

                markup = InlineKeyboardMarkup(row_width=2)
                btn_success = InlineKeyboardButton("✅ CONFIRMAR",callback_data=f"confirm-{bill.id}")
                btn_deny = InlineKeyboardButton("❌ DENEGAR",callback_data=f"deny-{bill.id}")
                markup.add(btn_success,btn_deny)
                bot.send_message(ADMIN1_ID,message,parse_mode="html",disable_web_page_preview=True,reply_markup=markup)
        except Exception as e:
            bot.send_message(ADMIN1_ID,f"⚠️ Ha ocurrido un error: {e}",parse_mode="html",disable_web_page_preview=True)





@bot.message_handler(content_types=["text"])
def bot_message_text(message):
    try:
        reply = message.reply_to_message

        if "COMPROBACION DE PAGO PARA BILL-" in reply.text and reply.reply_markup != None and message.chat.id == ADMIN1_ID:
            bot.send_chat_action(message.chat.id, "typing")

            liquidated = int(message.text)

            bill_id = int(reply.text.split(":")[0].replace("COMPROBACION DE PAGO PARA BILL-",""))            
            bill = Bill.objects.get(id=bill_id)
            bill.liquidated += liquidated

            if bill.liquidated >= bill.amount() + bill.revenue():
                bill.paid = True
                bill.save()
                bot.edit_message_text(reply.text + "\n\n✅ CONFIRMADO",message.chat.id,reply.id,parse_mode="html")

                bookings = Booking.objects.filter(bill = bill)

                booking_sends = []

                for booking in bookings:
                    if booking.reservationCode not in booking_sends:
                        headder = f"<b>ASIGNACION DE PNR PARA PASAJERO {booking.reservationCode}:</b>\n\n"
                        
                        message = f"<u>Datos del Vuelo de Ida:</u>\n"
                        message += f"<b>Fecha:</b> <code>{booking.flight.date}</code>\n"
                        message += f"<b>Origen:</b> <code>{booking.flight.begin}</code>\n"
                        message += f"<b>Destino:</b> <code>{booking.flight.to}</code>\n"
                        message += f"<b>Aerolinea:</b> <code>{booking.flight.aircraft.carrier_code}</code>\n"
                        message += f"<b>Charter:</b> <code>{booking.flight.charter}</code>\n"
                        message += f"<b>Avión:</b> <code>{booking.flight.aircraft}</code>\n"
                        message += f"<b>Número de Avión:</b> <code>{booking.flight.number}</code>\n"
                        message += f"<b>Hora de Salida:</b> <code>{booking.flight.departure}</code>\n"
                        message += f"<b>Hora de Llegada:</b> <code>{booking.flight.arrival}</code>\n\n"


                        if Booking.objects.filter(reservationCode=booking.reservationCode + 1).exists(): 
                            booking_return = Booking.objects.get(reservationCode=booking.reservationCode + 1)
                            message += f"<u>Datos del Vuelo de Regreso:</u>\n"
                            message += f"<b>Fecha:</b> <code>{booking_return.date}</code>\n"
                            message += f"<b>Origen:</b> <code>{booking_return.flight.begin}</code>\n"
                            message += f"<b>Destino:</b> <code>{booking_return.flight.to}</code>\n"
                            message += f"<b>Aerolinea:</b> <code>{booking_return.flight.aircraft.carrier_code}</code>\n"
                            message += f"<b>Charter:</b> <code>{booking_return.flight.charter}</code>\n"
                            message += f"<b>Avión:</b> <code>{booking_return.flight.aircraft}</code>\n"
                            message += f"<b>Número de Avión:</b> <code>{booking_return.flight.number}</code>\n"
                            message += f"<b>Hora de Salida:</b> <code>{booking_return.flight.departure}</code>\n"
                            message += f"<b>Hora de Llegada:</b> <code>{booking_return.flight.arrival}</code>\n\n"

                            
                            headder = f"<b>ASIGNACION DE PNR PARA PASAJERO {booking_return.reservationCode}:</b>\n\n"

                            booking_sends.append(booking_return.reservationCode)
                        
                        
                        message += f"<u>Datos Personales:</u>\n"
                        message += f"<b>Primer Nombre:</b> <code>{booking.firstName}</code>\n"
                        message += f"<b>Segundo Nombre:</b> <code>{booking.middleName}</code>\n"
                        message += f"<b>Primer Apellido:</b> <code>{booking.lastName}</code>\n"
                        message += f"<b>Segundo Apellido:</b> <code>{booking.motherLastName}</code>\n"
                        message += f"<b>Fecha de Nacimiento:</b> <code>{booking.birth}</code>\n"
                        message += f"<b>Genero:</b> <code>{booking.gender}</code>\n\n"
                        
                        message += f"<u>Documento Primario:</u>\n"
                        message += f"<b>Número:</b> <code>{booking.documentNumber}</code>\n"
                        message += f"<b>Expiración:</b> <code>{booking.documentExpiration}</code>\n"
                        message += f"<b>Tipo:</b> <code>{booking.documentType}</code>\n"
                        message += f"<b>País:</b> <code>{booking.documentCountry}</code>\n\n"
                        
                        message += f"<u>Documento Secundario:</u>\n"
                        message += f"<b>Número:</b> <code>{booking.secondaryDocumentNumber}</code>\n"
                        message += f"<b>Expiración:</b> <code>{booking.secondaryDocumentExpiration}</code>\n"
                        message += f"<b>Tipo:</b> <code>{booking.secondaryDocumentType}</code>\n"
                        message += f"<b>País:</b> <code>{booking.secondaryDocumentCountry}</code>\n"

                        message = headder + message
                        bot.send_message(ADMIN2_ID, message, parse_mode="html", disable_web_page_preview=True)

                        booking_sends.append(booking.reservationCode)

            else:
                bill.save()
                
                response = reply.text.split("Liquidado:")[0] + f"\n<b>Liquidado:</b> <code> ${bill.liquidated}</code>"

                bot.edit_message_text(response,message.chat.id,reply.id,parse_mode="html",reply_markup=reply.reply_markup)

        elif "✅ PNR ASIGNADO:" not in reply.text and "ASIGNACION DE PNR PARA PASAJERO" in reply.text and message.chat.id == ADMIN2_ID:
            bot.send_chat_action(message.chat.id, "typing")
            reservationCode = int(reply.text.split(":")[0].replace("ASIGNACION DE PNR PARA PASAJERO ",""))
            pnr = message.text
            if reservationCode%2 == 0:
                booking = Booking.objects.get(reservationCode=reservationCode - 1)
                booking.pnr = pnr
                booking_return = Booking.objects.get(reservationCode=reservationCode)
                booking_return.pnr = pnr
                booking.save()
                booking_return.save()
            else:
                booking = Booking.objects.get(reservationCode=reservationCode)
                booking.pnr = pnr
                booking.save()

            markup = InlineKeyboardMarkup(row_width=1)
            btnUrl = InlineKeyboardButton(booking.flight.charter.name,url=booking.flight.charter.url)
            markup.add(btnUrl)
            bot.edit_message_text(reply.text + "\n\n✅ PNR ASIGNADO:\n" + message.text,message.chat.id,reply.id,parse_mode="html",reply_markup=markup)

            if not Booking.objects.filter(bill = booking.bill, pnr = None).exists():
                threadSendMail = threading.Thread(name="threadSendMail", target=lambda:send_email_booking(booking.bill))
                threadSendMail.start()

    except Exception as e:
        bot.send_message(ADMIN1_ID,f"⚠️ Ha ocurrido un error: {e}",parse_mode="html",disable_web_page_preview=True)

    bot.delete_message(message.chat.id,message.id)



# ~ SEND MESSAGE ~
def send_email_booking(bill):
    bookings = Booking.objects.filter(bill = bill)
    booking_codes = []
    files = []
    recipient_list = []

    for booking in bookings:
        if booking.email not in recipient_list:recipient_list.append(booking.email)
        if booking.reservationCode not in booking_codes:
            b = [booking,]
            booking_return = Booking.objects.filter(reservationCode=booking.reservationCode + 1)
            
            if booking_return.exists(): 
                b.append(booking_return[0])
                booking_codes.append(booking_return[0].reservationCode)
            booking_codes.append(booking.reservationCode)
            
            file_path = str(settings.MEDIA_ROOT) + f'/{booking.name()}.pdf'

            try:os.remove(file_path)
            except:pass

            generate_tickets_pdf(b, booking.name())
            files.append(file_path)
        
        
            if booking.flight.baggagePolicy.baggagePolicy:
                file_path = str(settings.MEDIA_ROOT) + f'/{booking.flight.baggagePolicy.baggagePolicy}'
                files.append(file_path)

    
            
    subject = 'Notificación de voletos'
    from_email = settings.EMAIL_HOST_USER

    # Contenido HTML del correo electrónico
    context = {        
    }
    html_content = render_to_string('emails/email_notification_booking.html', context)
    text_content = strip_tags(html_content)

    # Crear el correo electrónico y adjuntar los archivos PDF
    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    email.attach_alternative(html_content, "text/html")
    for pdf_file in files:
        with open(pdf_file, 'rb') as file:
            pdf_data = file.read()
        email.attach(os.path.basename(pdf_file), pdf_data, 'application/pdf')
        
        try:os.remove(pdf_file)
        except:pass

    # Enviar el correo electrónico
    email.send()

def send_message_to_channel(message=str):
    bot.send_chat_action(CHANEL_ID, "typing")
    bot.send_message(CHANEL_ID,message,parse_mode="html",disable_web_page_preview=True)

    bot.send_chat_action(ADMIN1_ID, "typing")
    bot.send_message(ADMIN1_ID,message,parse_mode="html",disable_web_page_preview=True)

    bot.send_chat_action(ADMIN2_ID, "typing")
    bot.send_message(ADMIN2_ID,message,parse_mode="html",disable_web_page_preview=True)
    
def send_message_confirm_paid(message=str,bill=int):
    bot.send_chat_action(ADMIN1_ID, "typing")

    markup = InlineKeyboardMarkup(row_width=2)
    btn_success = InlineKeyboardButton("✅ CONFIRMAR",callback_data=f"confirm-{bill}")
    btn_deny = InlineKeyboardButton("❌ DENEGAR",callback_data=f"deny-{bill}")
    markup.add(btn_success,btn_deny)
    bot.send_message(ADMIN1_ID,message,parse_mode="html",disable_web_page_preview=True,reply_markup=markup)
    
def send_message_confirm_paid_package(message=str,bill=int):
    bot.send_chat_action(ADMIN1_ID, "typing")

    markup = InlineKeyboardMarkup(row_width=2)
    btn_success = InlineKeyboardButton("✅ CONFIRMAR",callback_data=f"confirm-package-{bill}")
    btn_deny = InlineKeyboardButton("❌ DENEGAR",callback_data=f"deny-package-{bill}")
    markup.add(btn_success,btn_deny)
    bot.send_message(ADMIN1_ID,message,parse_mode="html",disable_web_page_preview=True,reply_markup=markup)
    

def send_message_to_searchl_link(message=str):
    sl_id = -1001783822172
    bot.send_chat_action(sl_id, "typing")
    bot.send_message(sl_id,message,parse_mode="html",disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda x:True)
def response_buttons(call):
    try:
        chat_id = call.from_user.id
        message_id = call.message.id
        message_text = call.message.text
        bill_id = int(call.data.split("-")[1])

        if "confirm-package" in call.data and chat_id == ADMIN1_ID:
            bill = BillPackage.objects.get(id = bill_id)
            bill = Bill.objects.get(id = bill_id)
            bill.paid = True
            bill.liquidated = bill.amount() + bill.revenue()
            bill.save()

            bot.edit_message_text(message_text + "\n\n✅ CONFIRMADO",chat_id,message_id,parse_mode="html")
            
        elif "deny-package" in call.data and chat_id == ADMIN1_ID:
            bill = Bill.objects.get(id = bill_id)
            bill.paid = False
            bill.save()
            bot.edit_message_text(call.message.text + "\n\n❌ DENEGADO",chat_id,message_id,parse_mode="html")

        elif "confirm" in call.data and chat_id == ADMIN1_ID:
            bill = Bill.objects.get(id = bill_id)
            bill.paid = True
            bill.liquidated = bill.amount() + bill.revenue()
            bill.save()

            bot.edit_message_text(message_text + "\n\n✅ CONFIRMADO",chat_id,message_id,parse_mode="html")

            bookings = Booking.objects.filter(bill = bill)

            booking_sends = []

            for booking in bookings:
                if booking.reservationCode not in booking_sends:
                    headder = f"<b>ASIGNACION DE PNR PARA PASAJERO {booking.reservationCode}:</b>\n\n"
                    
                    message = f"<u>Datos del Vuelo de Ida:</u>\n"
                    message += f"<b>Fecha:</b> <code>{booking.flight.date}</code>\n"
                    message += f"<b>Origen:</b> <code>{booking.flight.begin}</code>\n"
                    message += f"<b>Destino:</b> <code>{booking.flight.to}</code>\n"
                    message += f"<b>Aerolinea:</b> <code>{booking.flight.aircraft.carrier_code}</code>\n"
                    message += f"<b>Charter:</b> <code>{booking.flight.charter}</code>\n"
                    message += f"<b>Avión:</b> <code>{booking.flight.aircraft}</code>\n"
                    message += f"<b>Número de Avión:</b> <code>{booking.flight.number}</code>\n"
                    message += f"<b>Hora de Salida:</b> <code>{booking.flight.departure}</code>\n"
                    message += f"<b>Hora de Llegada:</b> <code>{booking.flight.arrival}</code>\n\n"


                    if Booking.objects.filter(reservationCode=booking.reservationCode + 1).exists(): 
                        booking_return = Booking.objects.get(reservationCode=booking.reservationCode + 1)
                        message += f"<u>Datos del Vuelo de Regreso:</u>\n"
                        message += f"<b>Fecha:</b> <code>{booking_return.date}</code>\n"
                        message += f"<b>Origen:</b> <code>{booking_return.flight.begin}</code>\n"
                        message += f"<b>Destino:</b> <code>{booking_return.flight.to}</code>\n"
                        message += f"<b>Aerolinea:</b> <code>{booking_return.flight.aircraft.carrier_code}</code>\n"
                        message += f"<b>Charter:</b> <code>{booking_return.flight.charter}</code>\n"
                        message += f"<b>Avión:</b> <code>{booking_return.flight.aircraft}</code>\n"
                        message += f"<b>Número de Avión:</b> <code>{booking_return.flight.number}</code>\n"
                        message += f"<b>Hora de Salida:</b> <code>{booking_return.flight.departure}</code>\n"
                        message += f"<b>Hora de Llegada:</b> <code>{booking_return.flight.arrival}</code>\n\n"

                        
                        headder = f"<b>ASIGNACION DE PNR PARA PASAJERO {booking_return.reservationCode}:</b>\n\n"

                        booking_sends.append(booking_return.reservationCode)
                    
                    
                    message += f"<u>Datos Personales:</u>\n"
                    message += f"<b>Primer Nombre:</b> <code>{booking.firstName}</code>\n"
                    message += f"<b>Segundo Nombre:</b> <code>{booking.middleName}</code>\n"
                    message += f"<b>Primer Apellido:</b> <code>{booking.lastName}</code>\n"
                    message += f"<b>Segundo Apellido:</b> <code>{booking.motherLastName}</code>\n"
                    message += f"<b>Fecha de Nacimiento:</b> <code>{booking.birth}</code>\n"
                    message += f"<b>Genero:</b> <code>{booking.gender}</code>\n\n"
                    
                    message += f"<u>Documento Primario:</u>\n"
                    message += f"<b>Número:</b> <code>{booking.documentNumber}</code>\n"
                    message += f"<b>Expiración:</b> <code>{booking.documentExpiration}</code>\n"
                    message += f"<b>Tipo:</b> <code>{booking.documentType}</code>\n"
                    message += f"<b>País:</b> <code>{booking.documentCountry}</code>\n\n"
                    
                    message += f"<u>Documento Secundario:</u>\n"
                    message += f"<b>Número:</b> <code>{booking.secondaryDocumentNumber}</code>\n"
                    message += f"<b>Expiración:</b> <code>{booking.secondaryDocumentExpiration}</code>\n"
                    message += f"<b>Tipo:</b> <code>{booking.secondaryDocumentType}</code>\n"
                    message += f"<b>País:</b> <code>{booking.secondaryDocumentCountry}</code>\n"
                    
                    if booking.license:message += f"<b>Licensia:</b> <code>{booking.license}</code>\n"

                    message = headder + message
                    bot.send_message(ADMIN2_ID, message, parse_mode="html", disable_web_page_preview=True)

                    booking_sends.append(booking.reservationCode)

        elif "deny" in call.data and chat_id == ADMIN1_ID:
            bill = Bill.objects.get(id = bill_id)
            bill.paid = False
            bill.save()
            bot.edit_message_text(call.message.text + "\n\n❌ DENEGADO",chat_id,message_id,parse_mode="html")
    
    except Exception as e:
        bot.send_message(ADMIN1_ID,f"⚠️ Ha ocurrido un error: {e}",parse_mode="html",disable_web_page_preview=True)

def bot_infinity_polling():
    bot.infinity_polling()

#threadBot = threading.Thread(name="bot_infinity_polling", target=bot_infinity_polling)
#threadBot.start()

if not settings.DEBUG:
    try:
        bot.remove_webhook()
        ti.sleep(1)
        URL_WEBHOOK = os.environ.get('URL_WEBHOOK')
        bot.set_webhook(url=f"{URL_WEBHOOK}remote-control/")
    except:pass

