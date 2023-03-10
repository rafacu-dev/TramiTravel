import json
from datetime import date, datetime,timedelta
import threading
from os import remove
import os

from django.shortcuts import HttpResponse, redirect, render
from django.views.generic import View
from django.db.models import Q
from django.http import FileResponse, Http404
from apps.menus.models import Menu, Ofert, OfertGroup

from apps.reservations.models import BaggagePolicy, Bill, Booking, Destinatation, Flight

from apps.bot.bot import send_message_confirm_paid
from apps.utils.pdf_generated import generate_tickets_pdf
from apps.utils.countries import countries
from core.settings import BASE_DIR
from core.languages import get_strings

def date_key():
    dt_tuple = datetime.now().timetuple()
    year = str(dt_tuple.tm_year)[2:]
    day = str(dt_tuple.tm_yday)
    hour = dt_tuple.tm_hour * 60 * 60
    min = dt_tuple.tm_min * 60
    sec = str(hour + min + dt_tuple.tm_sec)

    for _ in range(len(sec),5):
        sec = "0" + sec

    for _ in range(len(day),3):
        day = "0" + day
    return year + day + sec
     

class Home(View):
    def get(self,request,*args,**kwargs):

        destinatations = Destinatation.objects.filter(actived=True)
        menus = Menu.objects.filter(actived=True).order_by('position')
        oferts = OfertGroup.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)
        
        context = {
            "oferts":oferts,
            "language":language,
            "strings" : strings,
            "destinatations" :destinatations,
            "menus" :menus
            }

        return render(request,'index.html',context)

class HomeTraslate(View):
    def get(self,request,traslate,*args,**kwargs):

        destinatations = Destinatation.objects.filter(actived=True)
        menus = Menu.objects.filter(actived=True).order_by('position')
        oferts = OfertGroup.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)
        
        context = {
            "traslate":"traslate",
            "oferts":oferts,
            "language":language,
            "strings" : strings,
            "destinatations" :destinatations,
            "menus" :menus
            }

        return render(request,'index.html',context)

class Flights(View):
    def get(self,request,*args,**kwargs):
        data = request.GET
        begin = int(data["begin"])
        to = int(data["to"])

        adults = int(data["adults"])
        children = int(data["children"])
        infants = int(data["infants"])

        ability_requiered = adults + children
        
        destinatations = Destinatation.objects.filter(actived=True)
        destinatationTo = destinatations.get(id = to)
        destinatationFrom = destinatations.get(id = begin)

        date_departure_select = data["date_departure"]
        date_departure_list = date_departure_select.split("/")
        date_departure = f"{date_departure_list[2]}-{date_departure_list[0]}-{date_departure_list[1]}"
        
        flights = list(Flight.objects.filter(date__gt=(datetime.now()),date=date_departure,begin=begin,to=to))
        for index, flight in enumerate(flights,start=0):
            if flight.capacity() < ability_requiered:
                flights.pop(index)

        available_dates = []

        if len(list(flights)) == 0:
            _flights = list(Flight.objects.filter(date__range=(datetime.now(), date_departure),begin=begin,to=to,actived=True).order_by("date").reverse())#.values('PlannedStartDateTime')
            for index, flight in enumerate(_flights,start=0):
                if flight.capacity() < ability_requiered:
                    _flights.pop(index)

            if len(list(_flights)) > 0:
                available_dates.append(_flights[0].date)
            
            dateDepartureObject = datetime(int(date_departure_list[2]),int(date_departure_list[0]),int(date_departure_list[1]))
            if dateDepartureObject >= datetime.now():
                _flights = list(Flight.objects.filter(date__gt=(date_departure),begin=begin,to=to,actived=True).order_by("date"))
                for index, flight in enumerate(_flights,start=0):
                    if flight.capacity() < ability_requiered:
                        _flights.pop(index)

                if len(list(_flights)) > 0:
                    available_dates.append(_flights[0].date)


        menus = Menu.objects.all().order_by('position')

        strings,language = get_strings(request.COOKIES)
        
        filter = f"{date_departure_select}  | {strings['from']}: {destinatationFrom.name()} {strings['to']}: {destinatationTo.name()}"

        context = {
            "language":language,
            "strings" : strings,
            "destinatations" :destinatations,
            "begin":begin - 1,
            "to":to - 1,
            "date_departure":date_departure_select,
            "flights":flights,
            "filter":filter,
            "adults":adults,
            "children":children,
            "infants":infants,
            "totalPassengers":adults + children + infants,
            "menus" :menus
            }
        if len(available_dates) > 0:
            context["available_dates"] = available_dates
            
        if "date_return" in data and data["date_return"] != "":
            date_return_select = data["date_return"]
            date_return_list = date_return_select.split("/")
            date_return = f"{date_return_list[2]}-{date_return_list[0]}-{date_return_list[1]}"
            
            flightsReturn = list(Flight.objects.filter(date=date_return,begin=to,to=begin,actived=True))
            for index, flight in enumerate(flightsReturn,start=0):
                if flight.capacity() < ability_requiered:
                    flightsReturn.pop(index)

            available_dates_return = []
            if len(list(flightsReturn)) == 0:
                
                _flights = list(Flight.objects.filter(date__range=(dateDepartureObject, date_return),begin=to,to=begin,actived=True).order_by("date").reverse())
                for index, flight in enumerate(_flights,start=0):
                    if flight.capacity() < ability_requiered:
                        _flights.pop(index)

                if len(list(_flights)) > 0:
                    available_dates_return.append(_flights[0].date)

                
                if datetime(int(date_return_list[2]),int(date_return_list[0]),int(date_return_list[1])) >= dateDepartureObject:
                    _flights = list(Flight.objects.filter(date__gt=(date_return),begin=to,to=begin).order_by("date"))
                    for index, flight in enumerate(_flights,start=0):
                        if flight.capacity() < ability_requiered:
                            _flights.pop(index)

                    if len(list(_flights)) > 0:
                        available_dates_return.append(_flights[0].date)

            if len(available_dates_return) > 0:
                context["available_dates_return"] = available_dates_return
            context["date_return"] = date_return_select
            context["flightsReturn"] = flightsReturn

        return render(request,'flight.html',context)

class GetFligths(View):
    def get(self,request,date_departure,date_return,begin,to,adults,children,infants,*args,**kwargs):
        if date_return == "none":
            date = date_departure
        else:
            date = date_return
        
        ability_requiered = adults + children
        data = []
        flights = Flight.objects.filter(date = date,begin=begin,to=to,actived=True)
        for f in flights:
            if f.capacity() >= ability_requiered:
                flight = {}
                flight["id"] = f.id
                flight["date"] = f.date.__str__()
                flight["ability"] = f.ability
                flight["price"] = f.priceAdultEC
                flight["actived"] = f.actived
                flight["priceMoney"] = f.priceMoney()

                flight["begin"] = f.begin.__str__()
                flight["to"] = f.to.__str__()

                #flight["airline"] = f.aircraft.carrier_code.name
                #flight["airlineImage"] = f.aircraft.carrier_code.image.url
                flight["airline"] = f.charter.name
                flight["airline_id"] = f.charter.id
                flight["airlineImage"] = f.charter.image.url

                flight["departure"] = f.departure.strftime("%I:%M:%p")
                flight["arrival"] = f.arrival.strftime("%I:%M:%p")
                flight["duration"] = f.duration()
                data.append(flight)

                if f.baggagePolicy:
                    flight["baggagePolicy"] = f.baggagePolicy.id

        returned = {
            "flights":data
        }

        if len(data) == 0:
            if date_return == "none":
                min_date = date_departure
                max_date = datetime.now()
            else:
                min_date = date_departure
                max_date = date_return

            _flights = list(Flight.objects.filter(date__range=(min_date, max_date),begin=begin,to=to).order_by("date").reverse())
            for index, flight in enumerate(_flights,start=0):
                if flight.capacity() < ability_requiered:
                    _flights.pop(index)

            available_dates = []
            if len(_flights) > 0:
                date = _flights[0].date
                available_dates.append([date.strftime("%Y"),date.strftime("%m"),date.strftime("%d")])

            
            _flights = list(Flight.objects.filter(date__gt=(max_date),begin=begin,to=to,actived=True).order_by("date"))
            for index, flight in enumerate(_flights,start=0):
                if flight.capacity() < ability_requiered:
                    _flights.pop(index)

            if len(list(_flights)) > 0:
                date = _flights[0].date
                available_dates.append([date.strftime("%Y"),date.strftime("%m"),date.strftime("%d")])
            
            
            returned["available_dates"] = available_dates
        flightsReturn = json.dumps(returned)
        return HttpResponse(flightsReturn,"application/json")

class Tickets(View):
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated: return  redirect("index")        

        tickets = Booking.objects.filter(user=request.user)
        
        compareTime = datetime.now() - timedelta(days = 1)
        
        for ticket in tickets:
            caduque_bill = Bill.objects.filter(Q(date__lte=compareTime),id = ticket.bill.id)
            if caduque_bill.exists():
                for b in caduque_bill:
                    b.delete()
                ticket.delete()

        bookings = []
        pending_bookings = []

        passengersCode = []
        bill = None

        for ticket in tickets:

            reservationCode = str(ticket.reservationCode)[:-2]
            if reservationCode not in passengersCode:
                passengersCode.append(reservationCode)
                data = {
                    "name":ticket.lastName + " " + ticket.motherLastName + ", " + ticket.firstName + " " + ticket.middleName,
                    "reservationCode":reservationCode
                }
                    
                if not ticket.bill.paid:
                    pending_bookings.append(data)
                    if bill == None:
                        bill = ticket.bill
                    else:
                        bill.amount += ticket.bill.amount
                        bill.code += f"-{ticket.bill.code}"
                else:
                    bookings.append(data)
    
        menus = Menu.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)

        select_booking = None
        if len(bookings) > 0:
            select_booking = bookings[0]["reservationCode"]
        elif len(pending_bookings) > 0:
            select_booking = pending_bookings[0]["reservationCode"]
            
        context = {
            "language":language,
            "strings" : strings,
            "menus" :menus,

            "tickets" : tickets,
            "bookings":bookings,
            "pending_bookings":pending_bookings,
            "bill":bill
            }

        if select_booking != None:context["select_booking"]=select_booking

        return render(request,'tickets.html',context)

    def post(self,request,*args,**kwargs):
        if not request.user.is_authenticated: return  redirect("index")
        data = request.POST
        try:
        
            codes = data["bill-code"].split("-")
            id = int(data["bill-id"])
            
            for code in codes:
                bill = Bill.objects.get(code = code, id = id)

                phone = data["phonePayment"]
                email = data["emailPayment"]
                if phone != "":
                    bill.zelle = phone
                elif email != "":
                    bill.zelle = email
                bill.paid = None
                bill.save()

                message = f"<b>Usurio:</b> <code>{request.user}</code>\n"
                message += f"<b>Zelle:</b> <code>{bill.zelle}</code>\n"
                message += f"<b>Codigo:</b> <code>{bill.code}</code>\n\n"
                message += f"<b>Monto requerido:</b> <code>{bill.amountMoney()}</code>"
                
                
                
                t = threading.Thread(target=lambda:send_message_confirm_paid(message,id))
                t.start()
            
            return  redirect("tickets")

        except: 
            print("Error al registrar pago")
            return  redirect("tickets")

class BookingView(View):
    def get(self,request,*args,**kwargs):
        data = request.GET

        adults = int(data['adults'])
        children = int(data['children'])
        infants = int(data['infants'])

        flightBegin = Flight.objects.get(id=data['flightBeginSelect'],actived=True)
        price = (flightBegin.priceAdultEC + flightBegin.revenueAdultEC) * adults
        price += (flightBegin.priceChildrenEC + flightBegin.revenueChildrenEC) * children
        price += (flightBegin.priceInfantEC + flightBegin.revenueInfantEC) * infants
        
        address_begin = countries[flightBegin.begin.countryCode.upper()]
        cities_begin = address_begin[0][list(address_begin[0].keys())[0]]
        address_to = countries[flightBegin.to.countryCode.upper()]
        cities_to = address_to[0][list(address_to[0].keys())[0]]
        
        
        menus = Menu.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)
        context = {
            "language":language,
            "strings" : strings,
            "address_begin" : address_begin,
            "cities_begin" : cities_begin,
            "address_to" : address_to,
            "cities_to" : cities_to,

            "flightBeginSelect" : flightBegin,

            "adults":data['adults'],
            "children":data['children'],
            "infants":data['infants'],
            "menus" :menus

            }

        if "flightReturnSelect" in data.keys():
            flightReturn = Flight.objects.get(id=data['flightReturnSelect'])
            context["flightReturnSelect"] = flightReturn
            price += (flightReturn.priceAdultEC + flightReturn.revenueAdultEC) * adults
            price += (flightReturn.priceChildrenEC + flightReturn.revenueChildrenEC) * children
            price += (flightReturn.priceInfantEC + flightReturn.revenueInfantEC) * infants

        if len(str(price).split(".")[1]) == 1: price = "$ " + str(price) + "0"
        else:price = "$ " + str(price)
        context['price'] = price
        return render(request,'booking.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST

        adults = int(data["adults"])
        children = int(data["children"])
        infants = int(data["infants"])

        passagersTypeList = ["Adult",]

        if children > 0 :passagersTypeList.append("Children")
        if infants > 0 :passagersTypeList.append("Infant")
        
        flightBeginSelect = int(data["flightBeginSelect"])
        flightBeginSelect = Flight.objects.get(id=flightBeginSelect)

        if "flightReturnSelect" in data.keys():
            flightReturnSelect = int(data["flightReturnSelect"])
            flightReturnSelect = Flight.objects.get(id=flightReturnSelect)
        else:
            flightReturnSelect = None

        
        dk = date_key()
        n = 1

        bill_pending = Booking.objects.filter(user = request.user, bill__paid = False)

        if bill_pending.exists():
            bill = bill_pending[0].bill
        else:
            bill = Bill.objects.create(code = str(dk[5:]))


        for p in passagersTypeList:
            if p == "Adult" :
                end = adults + 1
            elif p == "Children" :
                end = children + 1
            elif p == "Infant" :
                end = infants + 1


            for i in range(1, end):
                birthList = data[f'dateBirth-{p}{i}'].split("/")
                docExpList = data[f'primaryExpirationDocument-{p}{i}'].split("/")
                secDocExpList = data[f'secondaryExpirationDocument-{p}{i}'].split("/")
                
                if n < 10:_n = f"0{n}"
                else:_n = str(n)

                if p == "Adult" :
                    amount = flightBeginSelect.priceAdultEC
                    revenue = flightBeginSelect.revenueAdultEC
                elif p == "Children" :
                    amount = flightBeginSelect.priceChildrenEC
                    revenue = flightBeginSelect.revenueChildrenEC
                elif p == "Infant" :
                    amount = flightBeginSelect.priceInfantEC
                    revenue = flightBeginSelect.revenueInfantEC

                booking = Booking.objects.create(
                    user = request.user,
                    flight = flightBeginSelect,

                    firstName = data[f'firstName-{p}{i}'].upper(),
                    middleName = data[f'middleName-{p}{i}'].upper(),
                    lastName = data[f'lastName-{p}{i}'].upper(),
                    motherLastName = data[f'motherLastName-{p}{i}'].upper(),
                    birth = date(int(birthList[2]),int(birthList[0]),int(birthList[1])),
                    gender = data[f'gender-{p}{i}'].upper(),
                    
                    documentNumber = data[f'primaryDocumentNumber-{p}{i}'],
                    documentExpiration = date(int(docExpList[2]),int(docExpList[0]),int(docExpList[1])),
                    documentType = data[f'primaryDocumentType-{p}{i}'],
                    documentCountry = data[f'primaryCountryDocument-{p}{i}'],

                    email = data['emailContact'],
                    phone = data['codePhoneNumber'] + data['phoneNumber'],

                    streetBegin = data[f'address-street-1-{p}{i}'],
                    cityBegin = data[f'address-city-1-{p}{i}'],
                    stateBegin = data[f'address-state-1-{p}{i}'],

                    streetTo = data[f'address-street-2-{p}{i}'],
                    cityTo = data[f'address-city-2-{p}{i}'],
                    stateTo = data[f'address-state-2-{p}{i}'],

                    amount = amount,
                    revenue = revenue,

                    bill = bill,

                    reservationCode = dk + _n + "01"
                )

                if data[f'secondaryDocumentNumber-{p}{i}'] != "" and data[f'secondaryExpirationDocument-{p}{i}'] != "" and data[f'secondaryDocumentType-{p}{i}'] != "" and data[f'secondaryCountryDocument-{p}{i}']:
                    booking.secondaryDocumentNumber = data[f'secondaryDocumentNumber-{p}{i}']
                    booking.secondaryDocumentExpiration = date(int(secDocExpList[2]),int(secDocExpList[0]),int(secDocExpList[1]))
                    booking.secondaryDocumentType = data[f'secondaryDocumentType-{p}{i}']
                    booking.secondaryDocumentCountry = data[f'secondaryCountryDocument-{p}{i}']
                    booking.save()
                
                if flightReturnSelect != None:
                    if p == "Adult" :
                        amount = flightReturnSelect.priceAdultEC
                        revenue = flightReturnSelect.revenueAdultEC
                    elif p == "Children" :
                        amount = flightReturnSelect.priceChildrenEC
                        revenue = flightReturnSelect.revenueChildrenEC
                    elif p == "Infant" :
                        amount = flightReturnSelect.priceInfantEC
                        revenue = flightReturnSelect.revenueInfantEC

                    bookingReturn = Booking.objects.create(
                        user = request.user,
                        flight = flightReturnSelect,

                        firstName = data[f'firstName-{p}{i}'].upper(),
                        middleName = data[f'middleName-{p}{i}'].upper(),
                        lastName = data[f'lastName-{p}{i}'].upper(),
                        motherLastName = data[f'motherLastName-{p}{i}'].upper(),
                        birth = date(int(birthList[2]),int(birthList[0]),int(birthList[1])),
                        gender = data[f'gender-{p}{i}'].upper(),
                        
                        documentNumber = data[f'primaryDocumentNumber-{p}{i}'],
                        documentExpiration = date(int(docExpList[2]),int(docExpList[0]),int(docExpList[1])),
                        documentType = data[f'primaryDocumentType-{p}{i}'],
                        documentCountry = data[f'primaryCountryDocument-{p}{i}'],

                        email = data['emailContact'],
                        phone = data['codePhoneNumber'] + data['phoneNumber'],

                        streetBegin = data[f'address-street-1-{p}{i}'],
                        cityBegin = data[f'address-city-1-{p}{i}'],
                        stateBegin = data[f'address-state-1-{p}{i}'],

                        streetTo = data[f'address-street-2-{p}{i}'],
                        cityTo = data[f'address-city-2-{p}{i}'],
                        stateTo = data[f'address-state-2-{p}{i}'],

                        amount = amount,
                        revenue = revenue,

                        bill = bill,

                        reservationCode = dk + _n + "02"
                    )


                    if data[f'secondaryDocumentNumber-{p}{i}'] != "" and data[f'secondaryExpirationDocument-{p}{i}'] != "" and data[f'secondaryDocumentType-{p}{i}'] != "" and data[f'secondaryCountryDocument-{p}{i}']:
                        bookingReturn.secondaryDocumentNumber = data[f'secondaryDocumentNumber-{p}{i}']
                        bookingReturn.secondaryDocumentExpiration = date(int(secDocExpList[2]),int(secDocExpList[0]),int(secDocExpList[1]))
                        bookingReturn.secondaryDocumentType = data[f'secondaryDocumentType-{p}{i}']
                        bookingReturn.secondaryDocumentCountry = data[f'secondaryCountryDocument-{p}{i}']
                        bookingReturn.save()

                n += 1
        
        bill.save()

        bill.hoursRest()
        bill.minutesRest()
        bill.secondsRest()

        return  redirect("tickets")

class Message(View):
    def get(self,request,tag,*args,**kwargs):

        menus = Menu.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)
        ofert = Ofert.objects.get(tag=tag)
        if language == "en":
            message = ofert.message_en
        else:
            message = ofert.message_es

        context = {
            "language" : language,
            "strings" : strings,
            "menus" : menus,
            "messageOfert" : message,
            "imageOfert" : ofert.image.url
            }

        return render(request,'contact.html',context)

def baggagePolicy(request,bp):
    try:
        baggagePolicy = BaggagePolicy.objects.get(id=bp)        
        filepath = BASE_DIR + baggagePolicy.baggagePolicy.url
        
        pdf = open(filepath,"rb")
        pdf_return = pdf.read()
        pdf.close()
        
        return HttpResponse(pdf_return, content_type='application/pdf')
    
    except FileNotFoundError:
        raise Http404()
        
def download_pdf_ticket(request,tickets,option):
    #try:
        tickets = int(tickets + "01")
        bookings = Booking.objects.filter(Q(reservationCode = tickets)|Q(reservationCode = tickets + 1),actived=True)
        pdf_path = str(BASE_DIR) + "/media/reports/download_pdf_ticket.pdf"

        generate_tickets_pdf(bookings,pdf_path)

        pdf = open(pdf_path,"rb")
        pdf_return = pdf.read()
        pdf.close()

        remove(pdf_path)

        if option == 0:
            response = HttpResponse(pdf_return,content_type='application/pdf')
            response['Content-Disposition'] = f"attachment; filename=bookings.pdf"
            return response
        else:
            return HttpResponse(pdf_return, content_type='application/pdf')

    #except FileNotFoundError:
        raise Http404()

def deleteBooking(request):
    if request.method == 'POST':
        reservationCode = int(request.POST["reservationCode"] + "01")
        
        reservations = Booking.objects.filter(Q(reservationCode = reservationCode)|Q(reservationCode = reservationCode + 1))
        for reservation in reservations:
            reservation.delete()
        
        returned = {
            "success":"YES"
        }
        deleteReturn = json.dumps(returned)
        return HttpResponse(deleteReturn,"application/json")
    else:
        returned = {
            "success":"NO"
        }
        deleteReturn = json.dumps(returned)
        return HttpResponse(deleteReturn,"application/json")


"""import threading
import time as ti
def timer():
    while True:
        try:
            compareTime = datetime.now() - timedelta(days = 1)
            bills = Bill.objects.filter(Q(date__lte=compareTime))

            for bill in bills:
                bill.delete()

            ti.sleep(60)
        except:pass
        
t = threading.Thread(target=timer)
t.start()"""


