import json
from datetime import date, datetime, timedelta, time
import threading
from os import remove

from django.utils import timezone
from django.shortcuts import HttpResponse, redirect, render
from django.views.generic import View
from django.db.models import Q
from django.http import Http404
from apps.location.models import GetRequests
from apps.menus.models import Menu, Ofert, OfertGroup
from apps.reservations.forms import EditFlightForm, FlightForm

from apps.reservations.models import Aircraft, BaggagePolicy, Bill, Booking, Charter, ClassType, Destinatation, Flight, TvImages
from apps.hotels.models import Destinatation as DestinatationHotels, Hotel, RoomType, VacationPackage

from apps.bot.bot import send_message_confirm_paid
from apps.user.models import CreditRecharge
from apps.utils.pdf_generated import generate_tickets_pdf
from apps.utils.countries import countries
from core import settings
from core.settings import BASE_DIR
from core.languages import get_strings

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from apps.utils.utils import permission_checked

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
     


@method_decorator(permission_checked, name='dispatch')
class Home(View):
    def get(self,request,*args,**kwargs):
        
        try:
            ip_address = request.META.get('HTTP_CF_CONNECTING_IP')
            get_request, _ = GetRequests.objects.get_or_create(ip_address=ip_address)
            get_request.last_use = timezone.now()
            get_request.concurrence += 1
            get_request.save()
        except:pass

        relationsFrom = []
        relationsTo = []
        relationsHotels = []
        relationsRoomType = []

        fecha_actual = timezone.now().date()
        package = VacationPackage.objects.filter(Q(startDate__gte=fecha_actual) & Q(actived=True))

        for p in package:
            objFrom = {
                "id":p.origen.id,
                "name":p.origen.name(),
            }
            if objFrom not in relationsFrom:
                relationsFrom.append(objFrom)
                
            objTo = {
                "id_from":p.origen.id,
                "id":p.room.hotel.location.id,
                "name":p.room.hotel.location.name(),
            }
            if objTo not in relationsTo:
                relationsTo.append(objTo)
                
            objHotels = {
                "id_to":p.room.hotel.location.id,
                "id":p.room.hotel.id,
                "name":p.room.hotel.name,
                "max_adults":p.maxAdults(),
                "max_childrens":p.maxChildrens(),
                "max_infants":p.maxInfants(),

            }
            if objHotels not in relationsHotels:
                relationsHotels.append(objHotels)
                
            objRoomType = {
                "id_hotel":p.room.hotel.id,
                "id":p.room.room_type.id,
                "name":p.room.room_type.name,
            }
            if objRoomType not in relationsRoomType:
                relationsRoomType.append(objRoomType)


        destinatationsRelations = {
            "relationsFrom":relationsFrom,
            "relationsTo":relationsTo,
            "relationsHotels":relationsHotels,
            "relationsRoomType":relationsRoomType           
        }

        destinatations = Destinatation.objects.filter(actived=True)
        roomType = RoomType.objects.filter(actived=True)
        hotels = Hotel.objects.filter(actived=True)
        menus = Menu.objects.filter(actived=True).order_by('position')
        oferts = OfertGroup.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)
        
        context = {
            "oferts":oferts,
            "language":language,
            "strings" : strings,
            "destinatations" :destinatations,
            "destinatationsRelations":destinatationsRelations,
            "hotels":hotels,
            "roomType":roomType,
            "menus" :menus
            }

        return render(request,'index.html',context)

@method_decorator(permission_checked, name='dispatch')
class HomeTraslate(View):
    def get(self,request,traslate,*args,**kwargs):
        
        try:
            ip_address = request.META.get('HTTP_CF_CONNECTING_IP')
            get_request, _ = GetRequests.objects.get_or_create(ip_address=ip_address)
            get_request.last_use = timezone.now()
            get_request.concurrence += 1
            get_request.save()
        except:pass

        relationsFrom = []
        relationsTo = []
        relationsHotels = []
        relationsRoomType = []

        fecha_actual = timezone.now().date()
        package = VacationPackage.objects.filter(Q(startDate__gte=fecha_actual) & Q(actived=True))

        for p in package:
            objFrom = {
                "id":p.origen.id,
                "name":p.origen.name(),
            }
            if objFrom not in relationsFrom:
                relationsFrom.append(objFrom)
                
            objTo = {
                "id_from":p.origen.id,
                "id":p.room.hotel.location.id,
                "name":p.room.hotel.location.name(),
            }
            if objTo not in relationsTo:
                relationsTo.append(objTo)
                
            objHotels = {
                "id_to":p.room.hotel.location.id,
                "id":p.room.hotel.id,
                "name":p.room.hotel.name,
                "max_adults":p.maxAdults(),
                "max_childrens":p.maxChildrens(),
                "max_infants":p.maxInfants(),

            }
            if objHotels not in relationsHotels:
                relationsHotels.append(objHotels)
                
            objRoomType = {
                "id_hotel":p.room.hotel.id,
                "id":p.room.room_type.id,
                "name":p.room.room_type.name,
            }
            if objRoomType not in relationsRoomType:
                relationsRoomType.append(objRoomType)


        destinatationsRelations = {
            "relationsFrom":relationsFrom,
            "relationsTo":relationsTo,
            "relationsHotels":relationsHotels,
            "relationsRoomType":relationsRoomType           
        }

        destinatations = Destinatation.objects.filter(actived=True)
        roomType = RoomType.objects.filter(actived=True)
        hotels = Hotel.objects.filter(actived=True)
        menus = Menu.objects.filter(actived=True).order_by('position')
        oferts = OfertGroup.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)
        
        context = {
            "oferts":oferts,
            "language":language,
            "strings" : strings,
            "destinatations" :destinatations,
            "destinatationsRelations":destinatationsRelations,
            "hotels":hotels,
            "roomType":roomType,
            "menus" :menus
            }

        return render(request,'index.html',context)

@method_decorator(permission_checked, name='dispatch')
class Flights(View):
    def test_user(self):
        return self.request.user.is_authenticated and self.request.user.agency
    
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

        class_types = ClassType.objects.filter(actived=True).order_by('position')
        class_type = class_types[0]
        
        flights = list(Flight.objects.filter(date__gt=(datetime.now()),date=date_departure,begin=begin,to=to,actived=True,class_type=class_type.id))
        for index, flight in enumerate(flights,start=0):
            if flight.capacity() < ability_requiered:
                flights.pop(index)
            
            if self.test_user():flight.price_money = flight.priceAgencyMoney(revenue_agency=request.user.agency.revenue)
            else:flight.price_money = flight.priceMoney()

        available_dates = []

        dateDepartureObject = datetime(int(date_departure_list[2]),int(date_departure_list[0]),int(date_departure_list[1]))
        if len(list(flights)) == 0:
            _flights = list(Flight.objects.filter(date__range=(datetime.now(), date_departure),begin=begin,to=to,actived=True,class_type=class_type.id).order_by("date").reverse())#.values('PlannedStartDateTime')
            for index, flight in enumerate(_flights,start=0):
                if flight.capacity() < ability_requiered:
                    _flights.pop(index)

            if len(list(_flights)) > 0:
                available_dates.append(_flights[0].date)
            
            if dateDepartureObject >= datetime.now():
                _flights = list(Flight.objects.filter(date__gt=(date_departure),begin=begin,to=to,actived=True,class_type=class_type.id).order_by("date"))
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
            "begin":begin,
            "to":to,
            "date_departure":date_departure_select,
            "flights":flights,
            "filter":filter,
            "adults":adults,
            "children":children,
            "infants":infants,
            "totalPassengers":adults + children + infants,
            "menus" :menus,
            "class_types":class_types
            }
        if len(available_dates) > 0:
            context["available_dates"] = available_dates
            
        if "date_return" in data and data["date_return"] != "":
            date_return_select = data["date_return"]
            date_return_list = date_return_select.split("/")
            date_return = f"{date_return_list[2]}-{date_return_list[0]}-{date_return_list[1]}"
            
            flightsReturn = list(Flight.objects.filter(date=date_return,begin=to,to=begin,actived=True,class_type=class_type.id))
            for index, flight in enumerate(flightsReturn,start=0):
                if flight.capacity() < ability_requiered:
                    flightsReturn.pop(index)
            
                if self.test_user():flight.price_money = flight.priceAgencyMoney(revenue_agency=request.user.agency.revenue)
                else:flight.price_money = flight.priceMoney()

            available_dates_return = []
            if len(list(flightsReturn)) == 0:
                
                _flights = list(Flight.objects.filter(date__range=(dateDepartureObject, date_return),begin=to,to=begin,actived=True,class_type=class_type.id).order_by("date").reverse())
                for index, flight in enumerate(_flights,start=0):
                    if flight.capacity() < ability_requiered:
                        _flights.pop(index)

                if len(list(_flights)) > 0:
                    available_dates_return.append(_flights[0].date)

                
                if datetime(int(date_return_list[2]),int(date_return_list[0]),int(date_return_list[1])) >= dateDepartureObject:
                    _flights = list(Flight.objects.filter(date__gt=(date_return),begin=to,to=begin,class_type=class_type.id).order_by("date"))
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

@method_decorator(permission_checked, name='dispatch')
class GetFligths(View):
    def test_user(self):
        if self.request.user.is_authenticated and self.request.user.agency:return True
        return False
    
    def get(self,request,date_departure,date_return,begin,to,adults,children,infants,class_type,*args,**kwargs):

        if date_return == "none":
            date = date_departure
        else:
            date = date_return
        
        ability_requiered = adults + children
        data = []
        flights = Flight.objects.filter(date = date,begin=begin,to=to,actived=True,class_type=class_type)
        for f in flights:
            if f.capacity() >= ability_requiered:
                flight = {}
                flight["id"] = f.id
                flight["date"] = f.date.__str__()
                flight["ability"] = f.ability
                flight["price"] = f.priceAdult
                flight["actived"] = f.actived

                if self.test_user():flight["priceMoney"] = f.priceAgencyMoney(revenue_agency=request.user.agency.revenue)
                else:flight["priceMoney"] = f.priceMoney()

                flight["begin"] = f.begin.__str__()
                flight["to"] = f.to.__str__()

                flight["airline"] = f.charter.name
                flight["airline_id"] = f.charter.id
                flight["airlineImage"] = f.charter.image.url

                flight["departure"] = f.departure.strftime("%I:%M:%p")
                flight["arrival"] = f.arrival.strftime("%I:%M:%p")
                flight["duration"] = f.duration()
                flight["departureMS"] = f.departureMS()
                flight["arrivalMS"] = f.arrivalMS()
                data.append(flight)

                if f.baggagePolicy:
                    flight["baggagePolicy"] = f.baggagePolicy.id

        returned = {
            "flights":data
        }

        if len(data) == 0:
            print(date_return)
            if date_return == "none":
                min_date = datetime.now()
                max_date = date_departure
            else:
                min_date = date_departure
                max_date = date_return
                
            _flights = list(Flight.objects.filter(date__range=(min_date, max_date),begin=begin,to=to,actived=True,class_type=class_type).order_by("date").reverse())
            for index, flight in enumerate(_flights,start=0):
                if flight.capacity() < ability_requiered:
                    _flights.pop(index)

            available_dates = []
            if len(_flights) > 0:
                date = _flights[0].date
                available_dates.append([date.strftime("%Y"),date.strftime("%m"),date.strftime("%d")])

            
            _flights = list(Flight.objects.filter(date__gt=(max_date),begin=begin,to=to,actived=True,class_type=class_type).order_by("date"))
            for index, flight in enumerate(_flights,start=0):
                if flight.capacity() < ability_requiered:
                    _flights.pop(index)

            if len(list(_flights)) > 0:
                date = _flights[0].date
                available_dates.append([date.strftime("%Y"),date.strftime("%m"),date.strftime("%d")])
            
            
            returned["available_dates"] = available_dates
        flightsReturn = json.dumps(returned)
        return HttpResponse(flightsReturn,"application/json")

@method_decorator(permission_checked, name='dispatch')
class Bookingsagency(View):
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated: return  redirect("index")
        if not request.user.agency: return  redirect("tickets")

        menus = Menu.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)
        
        tickets = Booking.objects.filter(user=request.user)

        tickets_return = []
        for ticket in tickets:
            if not ticket.isReturn():
                ticket.amount_agency_money = ticket.amountagencyMoney(self.request.user.agency.revenue)
                ticket_return = Booking.objects.filter(reservationCode=ticket.reservationCode+1)
                if ticket_return:
                    ticket.flight_return = ticket_return.flight
                tickets_return.append(ticket)

        context = {
            "tickets":tickets_return,
            "language" : language,
            "strings" : strings,
            "menus" : menus,
            }

        return render(request,'bookings_agency.html',context)
    
    def post(self,request,*args,**kwargs):
        try:
            if not request.user.is_authenticated: return  redirect("index")

            if "amount_transferred" in request.POST.keys():
                phone = request.POST["phonePayment"]
                email = request.POST["emailPayment"]
                if phone != "":
                    zelle = phone
                elif email != "":
                    zelle = email

                CreditRecharge.objects.create(
                    zelle = zelle,
                    zelle_owner = request.POST["zelle-owner"],
                    amount = request.POST["amount_transferred"],
                    agency = request.user.agency,
                    user = request.user
                )

                menus = Menu.objects.filter(actived=True).order_by('position')
                strings,language = get_strings(request.COOKIES)
                
                tickets = Booking.objects.filter(user=request.user)

                tickets_return = []
                for ticket in tickets:
                    if not ticket.isReturn():
                        ticket.amount_agency_money = ticket.amountagencyMoney(self.request.user.agency.revenue)
                        ticket_return = Booking.objects.filter(reservationCode=ticket.reservationCode+1)
                        if ticket_return:
                            ticket.flight_return = ticket_return.flight
                        tickets_return.append(ticket)
                
                context = {
                    "tickets":tickets_return,
                    "language" : language,
                    "strings" : strings,
                    "menus" : menus,
                    }

                return render(request,'bookings_agency.html',context)


            booking = Booking.objects.get(user=request.user,id=int(request.POST["booking_id"]))

            if booking.amount + booking.flight.agencyCommission > request.user.agency.credit:
                returned = {
                    "success":"NO_CREDIT",
                }
                return HttpResponse(json.dumps(returned),"application/json")

            
            booking.liquidated = booking.amount + booking.flight.agencyCommission
            booking.save()
            

            request.user.agency.credit -= booking.amount + booking.flight.agencyCommission
            request.user.agency.save()

            
            returned = {
                "success":"YES",
                "amount_liquidated":booking.liquidatedMoney(),
                "total_credit":request.user.agency.creditMoney()
            }
            return HttpResponse(json.dumps(returned),"application/json")
        except:
            returned = {
                "success":"NO",
            }
            return HttpResponse(json.dumps(returned),"application/json")
        
@method_decorator(permission_checked, name='dispatch')
class Tickets(View):
    
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated: return  redirect("index") 
        if self.request.user.agency:return redirect("bookingsagency")

        menus = Menu.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)
        

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
                        #bill.amount += ticket.bill.amount
                        bill.code += f"-{ticket.bill.code}"
                else:
                    bookings.append(data)
    

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
                bill.zelle_owner = data["zelle-owner"]
                bill.paid = None
                bill.save()

                message = f"<b>COMPROBACION DE PAGO PARA BILL-{bill.id}:</b>\n\n"
                message += f"<b>Usuario:</b> <code>{request.user}</code>\n"
                message += f"<b>Zelle:</b> <code>{bill.zelle}</code>\n"
                message += f"<b>Codigo:</b> <code>{bill.code}</code>\n\n"
                message += f"<b>Monto requerido:</b> <code>{bill.amountMoney()}</code>\n"
                message += f"<b>Liquidado:</b> <code> ${bill.liquidated}</code>"
                
                
                
                t = threading.Thread(target=lambda:send_message_confirm_paid(message,id))
                t.start()
            
            return  redirect("tickets")

        except: 
            print("Error al registrar pago")
            return  redirect("tickets")

@method_decorator(permission_checked, name='dispatch')
class BookingView(View):
    def test_user(self):
        return self.request.user.is_authenticated and self.request.user.agency
    
    def get(self,request,*args,**kwargs):
        data = request.GET

        adults = int(data['adults'])
        children = int(data['children'])
        infants = int(data['infants'])

        flightBegin = Flight.objects.get(id=data['flightBeginSelect'],actived=True)
        price = (flightBegin.priceAdult + flightBegin.revenueAdult) * adults
        price += (flightBegin.priceChildren + flightBegin.revenueChildren) * children
        price += (flightBegin.priceInfant + flightBegin.revenueInfant) * infants
        
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
            price += (flightReturn.priceAdult + flightReturn.revenueAdult) * adults
            price += (flightReturn.priceChildren + flightReturn.revenueChildren) * children
            price += (flightReturn.priceInfant + flightReturn.revenueInfant) * infants

        if len(str(price).split(".")[1]) == 1: price = "$ " + str(price) + "0"
        else:price = "$ " + str(price)
        context['price'] = price
        return render(request,'booking.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        files = request.FILES
        

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
                docExpList = data[f'expiration-document-primary-{p}{i}'].split("/")
                secDocExpList = data[f'expiration-document-secondary-{p}{i}'].split("/")
                
                if n < 10:_n = f"0{n}"
                else:_n = str(n)

                if p == "Adult" :
                    amount = flightBeginSelect.priceAdult
                    revenue = flightBeginSelect.revenueAdult
                elif p == "Children" :
                    amount = flightBeginSelect.priceChildren
                    revenue = flightBeginSelect.revenueChildren
                elif p == "Infant" :
                    amount = flightBeginSelect.priceInfant
                    revenue = flightBeginSelect.revenueInfant

                booking = Booking.objects.create(
                    user = request.user,
                    flight = flightBeginSelect,

                    firstName = data[f'firstName-{p}{i}'].upper(),
                    middleName = data[f'middleName-{p}{i}'].upper(),
                    lastName = data[f'lastName-{p}{i}'].upper(),
                    motherLastName = data[f'motherLastName-{p}{i}'].upper(),
                    birth = date(int(birthList[2]),int(birthList[0]),int(birthList[1])),
                    gender = data[f'gender-{p}{i}'].upper(),
                    
                    documentNumber = data[f'number-document-primary-{p}{i}'],
                    documentExpiration = date(int(docExpList[2]),int(docExpList[0]),int(docExpList[1])),
                    documentType = data[f'type-document-primary-{p}{i}'],
                    documentCountry = data[f'country-document-primary-{p}{i}'],

                    email = data['emailContact'],
                    phone = data['codePhoneNumber'] + data['phoneNumber'],

                    streetBegin = data[f'address-street-1'],
                    cityBegin = data[f'address-city-1'],
                    stateBegin = data[f'address-state-1'],

                    streetTo = data[f'address-street-2'],
                    cityTo = data[f'address-city-2'],
                    stateTo = data[f'address-state-2'],

                    amount = amount,
                    revenue = revenue,

                    bill = bill,

                    reservationCode = dk + _n + "01"
                )
                
                if f"license-{p}{i}" in files.keys():
                    booking.license = data[f'license-{p}{i}']
                    booking.save()
                
                if f"imagen-document-{p}{i}" in files.keys():
                    image  = files[f"imagen-document-{p}{i}"]
                    imageName = f"primary_document_" + str(booking.id) + ".png"
                    booking.imageDocument.save(imageName,image)

                if data[f'number-document-secondary-{p}{i}'] != "" and data[f'expiration-document-secondary-{p}{i}'] != "" and data[f'type-document-secondary-{p}{i}'] != "" and data[f'country-document-secondary-{p}{i}']:
                    booking.secondaryDocumentNumber = data[f'number-document-secondary-{p}{i}']
                    booking.secondaryDocumentExpiration = date(int(secDocExpList[2]),int(secDocExpList[0]),int(secDocExpList[1]))
                    booking.secondaryDocumentType = data[f'type-document-secondary-{p}{i}']
                    booking.secondaryDocumentCountry = data[f'country-document-secondary-{p}{i}']
                    booking.save()
                    
                    if f"imagen-document-secondary-{p}{i}" in files.keys():
                        image  = files[f"imagen-document-secondary-{p}{i}"]
                        imageName = f"secondary_document_" + str(booking.id) + ".png"
                        booking.imageSecondaryDocument.save(imageName,image)
                
                if flightReturnSelect != None:
                    if p == "Adult" :
                        amount = flightReturnSelect.priceAdult
                        revenue = flightReturnSelect.revenueAdult
                    elif p == "Children" :
                        amount = flightReturnSelect.priceChildren
                        revenue = flightReturnSelect.revenueChildren
                    elif p == "Infant" :
                        amount = flightReturnSelect.priceInfant
                        revenue = flightReturnSelect.revenueInfant

                    bookingReturn = Booking.objects.create(
                        user = request.user,
                        flight = flightReturnSelect,

                        firstName = data[f'firstName-{p}{i}'].upper(),
                        middleName = data[f'middleName-{p}{i}'].upper(),
                        lastName = data[f'lastName-{p}{i}'].upper(),
                        motherLastName = data[f'motherLastName-{p}{i}'].upper(),
                        birth = date(int(birthList[2]),int(birthList[0]),int(birthList[1])),
                        gender = data[f'gender-{p}{i}'].upper(),
                        
                        documentNumber = data[f'number-document-primary-{p}{i}'],
                        documentExpiration = date(int(docExpList[2]),int(docExpList[0]),int(docExpList[1])),
                        documentType = data[f'type-document-primary-{p}{i}'],
                        documentCountry = data[f'country-document-primary-{p}{i}'],

                        email = data['emailContact'],
                        phone = data['codePhoneNumber'] + data['phoneNumber'],

                        streetBegin = data[f'address-street-1'],
                        cityBegin = data[f'address-city-1'],
                        stateBegin = data[f'address-state-1'],

                        streetTo = data[f'address-street-2'],
                        cityTo = data[f'address-city-2'],
                        stateTo = data[f'address-state-2'],

                        amount = amount,
                        revenue = revenue,

                        bill = bill,

                        reservationCode = dk + _n + "02"
                    )


                    if f"license-{p}{i}" in files.keys():
                        bookingReturn.license = data[f'license-{p}{i}']
                        bookingReturn.save()

                    if f"imagen-document-{p}{i}" in files.keys():
                        image  = files[f"imagen-document-{p}{i}"]
                        imageName = f"primary_document_" + str(bookingReturn.id) + ".png"
                        bookingReturn.imageDocument.save(imageName,image)

                    if data[f'number-document-secondary-{p}{i}'] != "" and data[f'expiration-document-secondary-{p}{i}'] != "" and data[f'type-document-secondary-{p}{i}'] != "" and data[f'country-document-secondary-{p}{i}']:
                        bookingReturn.secondaryDocumentNumber = data[f'number-document-secondary-{p}{i}']
                        bookingReturn.secondaryDocumentExpiration = date(int(secDocExpList[2]),int(secDocExpList[0]),int(secDocExpList[1]))
                        bookingReturn.secondaryDocumentType = data[f'type-document-secondary-{p}{i}']
                        bookingReturn.secondaryDocumentCountry = data[f'country-document-secondary-{p}{i}']
                        bookingReturn.save()

                        if f"imagen-document-secondary-{p}{i}" in files.keys():
                            image  = files[f"imagen-document-secondary-{p}{i}"]
                            imageName = f"secondary_document_" + str(bookingReturn.id) + ".png"
                            bookingReturn.imageSecondaryDocument.save(imageName,image)

                n += 1
        
        bill.save()

        bill.hoursRest()
        bill.minutesRest()
        bill.secondsRest()

        return  redirect("tickets")

@method_decorator(permission_checked, name='dispatch')
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

@method_decorator(permission_checked, name='dispatch')
class AddFlight(View):
    def test_user(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def get(self,request,*args,**kwargs):
        if not self.test_user():
            return redirect('index')
        
        menus = Menu.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)
        form = FlightForm()
        class_type = ClassType.objects.filter(actived=True).order_by('position')
        bp = BaggagePolicy.objects.filter(actived=True)

        context = {
            "language" : language,
            "strings" : strings,
            "menus" : menus,
            "form":form,
            "class_type":class_type,
            "bp":bp
            }

        return render(request,'add_flight.html',context)

    def post(self,request,*args,**kwargs):
        if not self.test_user():
            return redirect('index')
        
        form = FlightForm(request.POST)

        departure_h = int(request.POST["departure_h"])
        departure_m = int(request.POST["departure_m"])
        arrival_h = int(request.POST["arrival_h"])
        arrival_m = int(request.POST["arrival_m"])

        class_type = ClassType.objects.filter(actived=True).order_by('position')
        bp = BaggagePolicy.objects.filter(actived=True)
        
        if form.is_valid():
            date_flights = request.POST["days_flights"].split(',')
            for d in date_flights:
                d = d.split("-")

                for c in class_type:
                    if f'class_type_{c.id}' in request.POST.keys() and request.POST[f'class_type_{c.id}'] == 'on':
                        Flight.objects.create(
                            begin = form.cleaned_data['begin'],
                            to = form.cleaned_data['to'],
                            gate = form.cleaned_data['gate'],
                            charter = form.cleaned_data['charter'],
                            aircraft = form.cleaned_data['aircraft'],
                            number = form.cleaned_data['number'],
                            checkinMoment = form.cleaned_data['checkinMoment'],
                            departure = time(hour=departure_h, minute=departure_m),
                            arrival = time(hour=arrival_h, minute=arrival_m),
                            date = date(int(d[0]), int(d[1]), int(d[2])),

                            ability = request.POST[f'ability{c.id}'],
                            priceAdult = request.POST[f'priceAdult{c.id}'],
                            revenueAdult = request.POST[f'revenueAdult{c.id}'],
                            priceChildren = request.POST[f'priceChildren{c.id}'],
                            revenueChildren = request.POST[f'revenueChildren{c.id}'],
                            priceInfant = request.POST[f'priceInfant{c.id}'],
                            revenueInfant = request.POST[f'revenueInfant{c.id}'],
                            agencyCommission = form.cleaned_data['agencyCommission'],

                            baggagePolicy = BaggagePolicy.objects.get(id=request.POST[f'baggagePolicy{c.id}']),
                            class_type = ClassType.objects.get(id=request.POST[f'class_type_val_{c.id}'])
                        )
        else:
            print("Formulario no valido")

        menus = Menu.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)
        form = FlightForm()

        context = {
            "language" : language,
            "strings" : strings,
            "menus" : menus,
            "form":form,
            "class_type":class_type,
            "bp":bp
            }

        return render(request,'add_flight.html',context)

@method_decorator(permission_checked, name='dispatch')
class EditFlights(View):
    def test_user(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def get(self,request,flight_ids,*args,**kwargs):
        if not self.test_user():
            return redirect('index')
        
        menus = Menu.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)

        form = EditFlightForm()
        class_type = ClassType.objects.filter(actived=True).order_by('position')
        bp = BaggagePolicy.objects.filter(actived=True)
        flights = []

        flight_ids_list = flight_ids.split("-")

        for id in flight_ids_list:
            flights.append(Flight.objects.get(id=id))
        

        context = {
            "language" : language,
            "strings" : strings,
            "menus" : menus,
            "form":form,
            "class_type":class_type,
            "bp":bp,
            "flights":flights
            }

        return render(request,'edit_flight.html',context)


    def post(self,request,*args,**kwargs):
        if not self.test_user():
            return redirect('index')
        
        data = dict(request.POST)
        flight_ids = data['flight_ids']
        edited_fields = data['edited_fields']
        form = EditFlightForm(request.POST)
        form.is_valid()

        for id in flight_ids:
            flight = Flight.objects.get(id=id)
            for field in edited_fields:
                if field == "begin":
                    flight.begin = form.cleaned_data["begin"]
                elif field == "to":
                    flight.to = form.cleaned_data["to"]
                elif field == "gate":
                    flight.gate = form.cleaned_data["gate"]
                elif field == "charter":
                    flight.charter = form.cleaned_data["charter"]
                elif field == "aircraft":
                    flight.aircraft = form.cleaned_data["aircraft"]
                elif field == "number":
                    flight.number = form.cleaned_data["number"]
                elif field == "checkinMoment":
                    flight.checkinMoment = form.cleaned_data["checkinMoment"]
                elif field == "departure":
                    departure_h = int(request.POST["departure_h"])
                    departure_m = int(request.POST["departure_m"])                    
                    flight.departure = time(hour=departure_h, minute=departure_m)
                elif field == "arrival":
                    arrival_h = int(request.POST["arrival_h"])
                    arrival_m = int(request.POST["arrival_m"])                    
                    flight.arrival = time(hour=arrival_h, minute=arrival_m)
                elif field == "date":                    
                    d = data["date"][0].split("/")
                    print(d)
                    flight.date = date(int(d[2]), int(d[0]),int(d[1]))
                elif field == "ability":
                    flight.ability = form.cleaned_data["ability"]
                elif field == "priceAdult":
                    flight.priceAdult = form.cleaned_data["priceAdult"]
                elif field == "revenueAdult":
                    flight.revenueAdult = form.cleaned_data["revenueAdult"]
                elif field == "priceChildren":
                    flight.priceChildren = form.cleaned_data["priceChildren"]
                elif field == "revenueChildren":
                    flight.revenueChildren = form.cleaned_data["revenueChildren"]
                elif field == "priceInfant":
                    flight.priceInfant = form.cleaned_data["priceInfant"]
                elif field == "revenueInfant":
                    flight.revenueInfant = form.cleaned_data["revenueInfant"]
                elif field == "agencyCommission":
                    flight.agencyCommission = form.cleaned_data["agencyCommission"]
                elif field == "class_type":
                    flight.class_type = form.cleaned_data["class_type"]
                elif field == "baggagePolicy":
                    flight.baggagePolicy = form.cleaned_data["baggagePolicy"]
                flight.save()

        return redirect("/admin/reservations/flight/")

def baggagePolicy(request,bp):
    try:
        baggagePolicy = BaggagePolicy.objects.get(id=bp)        
        filepath = str(BASE_DIR) + baggagePolicy.baggagePolicy.url
        
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
        file_path = str(settings.MEDIA_ROOT) + '/download_pdf_ticket.pdf'

        try:remove(file_path)
        except:pass

        generate_tickets_pdf(bookings,"download_pdf_ticket")

        pdf = open(file_path,"rb")
        pdf_return = pdf.read()
        pdf.close()

        try:remove(file_path)
        except:pass

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


def terminosCondiciones(request):
    try:        
        pdf = open("static/docs/terminos_condiciones.pdf","rb")
        pdf_return = pdf.read()
        pdf.close()
        
        return HttpResponse(pdf_return, content_type='application/pdf')
    
    except FileNotFoundError:
        raise Http404()


def politicaPrivacidad(request):
    try:
        pdf = open("static/docs/politica_privacidad.pdf","rb")
        pdf_return = pdf.read()
        pdf.close()
        
        return HttpResponse(pdf_return, content_type='application/pdf')
    
    except FileNotFoundError:
        raise Http404()
    
    
class Tv(View):
    def get(self,request,*args,**kwargs):
        images = TvImages.objects.all()
        return render(request,'tv.html',{"images":images,"image":list(images)[-1]})


class CitiesView(View):
    def get(self,request,*args,**kwargs):
        data = request.GET

        adults = int(data['adults'])
        
        
        menus = Menu.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)
        context = {}
        return render(request,'booking.html',context)

def getStatesView(request,name):
    with open('apps/menus/countries-states-cities.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    names = []
    
    for item in data:
        if 'name' in item and item['name'] == name:
            for state in item["states"]:
                if 'name' in state:names.append(state['name'])
            break
    data =json.dumps({"names":names})
    return HttpResponse("application/json")

@method_decorator(csrf_exempt, name='dispatch')
def getCitiesView(request):
    cuntry = request.POST.get("countrie")
    state_name = request.POST.get("state")  
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
    data =json.dumps({"names":names})
    return HttpResponse(data,"application/json")
