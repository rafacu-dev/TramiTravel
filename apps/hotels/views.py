import calendar
from datetime import date, datetime, timedelta
import threading
from apps.user.models import CreditRecharge
from apps.utils.countries import countries
from django.shortcuts import redirect, render
from django.views.generic import View
from django.utils.decorators import method_decorator
from apps.hotels.models import Bill, Booking, Client, Destinatation, Hotel, RoomType, VacationPackage

from apps.menus.models import Menu
from apps.utils.utils import toMoney,permission_checked
from core.languages import get_strings

from apps.bot.bot import send_message_confirm_paid_package


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
class Hotels(View):
    def get(self,request,*args,**kwargs):
        data = request.GET
        nearest_airport = int(data["begin"])
        to = int(data["to"])
        room_type = data["room-type"]
        hotel = data["hotel"]

        rooms_clients = str(data["room-clients"]).split("%")[:-1]

        month_year = data["month-travel"]

        
        # Convertir el mes y año proporcionados a un objeto de fecha
        start_day = datetime.strptime(month_year, '%Y-%m').date().replace(day=1)
        last_day = start_day.replace(day=calendar.monthrange(start_day.year, start_day.month)[1])

        period_packages = VacationPackage.objects.filter(
            #package__hotel__id = hotel,
            origen__id = nearest_airport,
            startDate__range = (start_day,last_day)
        ).distinct()
        if room_type != "All":period_packages = period_packages.filter(room__room_type__id = room_type,).distinct()
        
        
        for pp in period_packages:
            priceTotal = 0.0
            for room in rooms_clients:
                clients = room.split("-")
                priceTotal += pp.priceTotal(int(clients[0]),int(clients[1]),int(clients[2]))

            pp.priceTotalM = toMoney(priceTotal)

        strings,language = get_strings(request.COOKIES)
        
        destinatationsHotels = Destinatation.objects.filter(actived=True)
        menus = Menu.objects.filter(actived=True).order_by('position')
        
        context = {
            "room_clients":data["room-clients"],
            "language":language,
            "strings" : strings,
            "destinatationsHotels":destinatationsHotels,
            "menus" :menus,
            'period_packages': period_packages
            }
            
        return render(request,'hotels.html',context)
    
    
@method_decorator(permission_checked, name='dispatch')
class ReservationsView(View):
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated: return  redirect("index") 
        if self.request.user.agency:return redirect("reservationsagency")

        data = request.GET
        menus = Menu.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)

        package_ids = []
        reservations = []

        bookings = Booking.objects.filter(user = request.user, actived = True)
        

        bill = None

        for booking in bookings:
            if  bill == None: bill = booking.bill

            package_id = booking.package.id
            total_amount = 0.0

            if package_id not in package_ids:
                package_ids.append(package_id)

                rooms_dict = {}
                amounts_dict = {}
                for room in bookings.filter(package = booking.package):
                        clients = Client.objects.filter(booking=room)
                        for client in clients:
                            if room.reservationCode in rooms_dict.keys():
                                rooms_dict[room.reservationCode].append({
                                "firstName":client.firstName,
                                "middleName":client.middleName,
                                "lastName":client.lastName,
                                "motherLastName":client.motherLastName,
                                "birth":client.birth,
                                "gender":client.gender,
                                "documentNumber":client.documentNumber
                                })
                            else:
                                rooms_dict[room.reservationCode] = [{
                                "firstName":client.firstName,
                                "middleName":client.middleName,
                                "lastName":client.lastName,
                                "motherLastName":client.motherLastName,
                                "birth":client.birth,
                                "gender":client.gender,
                                "documentNumber":client.documentNumber
                                }]
                                amounts_dict[room.reservationCode] = room.amount
                                total_amount +=room.amount
                rooms = []
                for key in rooms_dict.keys():
                    rooms.append([rooms_dict[key],amounts_dict[key],key])
                
                booking.rooms = rooms
                booking.total_amount = total_amount
                reservations.append(booking)

        context = {
            "language":language,
            "strings" : strings,
            "menus" :menus,
            "reservations":reservations,
            "bill":bill
            }
        
        return render(request,'reservations_package.html',context)
    
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

                message = f"<b>COMPROBACION DE PAGO DE PAQUETE CON BILL-{bill.id}:</b>\n\n"
                message += f"<b>Usuario:</b> <code>{request.user}</code>\n"
                message += f"<b>Zelle:</b> <code>{bill.zelle}</code>\n"
                message += f"<b>Codigo:</b> <code>{bill.code}</code>\n\n"
                message += f"<b>Monto requerido:</b> <code>{bill.amountMoney()}</code>\n"
                message += f"<b>Liquidado:</b> <code> ${bill.liquidated}</code>"
                
                
                
                t = threading.Thread(target=lambda:send_message_confirm_paid_package(message,id))
                t.start()
            
            return  redirect("reservations")

        except: 
            print("Error al registrar pago")
            return  redirect("reservations")
        
    
@method_decorator(permission_checked, name='dispatch')
class ReservationsagencyView(View):
    def get(self,request,*args,**kwargs):
        data = request.GET
        menus = Menu.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)

        bookings = Booking.objects.filter(user = request.user)

        if "start_date" in data.keys() and data["start_date"] != "":
            start_date = datetime.strptime(data["start_date"], '%m/%d/%Y')
            bookings = bookings.filter(date__gt=start_date)

        if "end_date" in data.keys() and data["end_date"] != "":
            end_date = datetime.strptime(data["end_date"], '%m/%d/%Y')
            bookings = bookings.filter(date__lt=end_date)
        
        if "booking_code" in data.keys() and data["booking_code"] != "":
            bookings = bookings.filter(reservationCode=data["booking_code"])
        
        if "booking_holder" in data.keys() and data["booking_holder"] != "":
            bookings = bookings.filter(id__in=[b.id for b in bookings if data["booking_holder"].lower() in b.holder().lower()])
            

        bookings = bookings.distinct()


        
        package_ids = []
        reservations = []

        bill = None

        for booking in bookings:
            if  bill == None: bill = booking.bill

            package_id = booking.package.id
            total_amount = 0.0

            rooms_dict = {}
            amounts_dict = {}
            for room in bookings.filter(package = booking.package):
                    clients = Client.objects.filter(booking=room)
                    for client in clients:
                        if room.reservationCode in rooms_dict.keys():
                            rooms_dict[room.reservationCode].append({
                            "firstName":client.firstName,
                            "middleName":client.middleName,
                            "lastName":client.lastName,
                            "motherLastName":client.motherLastName,
                            "birth":client.birth,
                            "gender":client.gender,
                            "documentNumber":client.documentNumber
                            })
                        else:
                            rooms_dict[room.reservationCode] = [{
                            "firstName":client.firstName,
                            "middleName":client.middleName,
                            "lastName":client.lastName,
                            "motherLastName":client.motherLastName,
                            "birth":client.birth,
                            "gender":client.gender,
                            "documentNumber":client.documentNumber
                            }]
                            amounts_dict[room.reservationCode] = room.amount
                            total_amount +=room.amount
            rooms = []
            for key in rooms_dict.keys():
                rooms.append([rooms_dict[key],amounts_dict[key],key])
            
            booking.rooms = rooms
            booking.total_amount = total_amount
            reservations.append(booking)


        context = {
            "language":language,
            "strings" : strings,
            "menus" :menus,
            "bookings":reservations,
            "bill":bill
            }
        if "start_date" in data.keys():context["start_date"] = data["start_date"]
        if "end_date" in data.keys():context["end_date"] = data["end_date"]
        if "booking_code" in data.keys():context["booking_code"] = data["booking_code"]
        if "booking_holder" in data.keys():context["booking_holder"] = data["booking_holder"]
        
        return render(request,'reservations_package_agency.html',context)
        
    def post(self,request,*args,**kwargs):
        data = request.POST
        if "cancel-booking-id" in data.keys():
            booking = Booking.objects.get(user = request.user,id=data["cancel-booking-id"])
            booking.actived = False
            booking.save()

        if "liquidated-booking-id" in data.keys():
            amount = float(data["liquidated-booking-amount"])
            booking = Booking.objects.get(user = request.user,id=data["liquidated-booking-id"])
            booking.liquidated += amount
            booking.save()

            request.user.agency.credit -= amount
            request.user.agency.save()
        
        if "amount_transferred" in data.keys():
            phone = data["phonePayment"]
            email = data["emailPayment"]
            if phone != "":
                zelle = phone
            elif email != "":
                zelle = email

            CreditRecharge.objects.create(
                zelle = zelle,
                zelle_owner = data["zelle-owner"],
                amount = data["amount_transferred"],
                agency = request.user.agency,
                user = request.user
            )


        menus = Menu.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)

        bookings = Booking.objects.filter(user = request.user)

        context = {
            "language":language,
            "strings" : strings,
            "menus" :menus,
            "bookings":bookings,
            "total_credit":request.user.agency.creditMoney()
            }
        
        return render(request,'reservations_package_agency.html',context)


@method_decorator(permission_checked, name='dispatch')        
class BookingView(View):
    
    def get(self,request,*args,**kwargs):
        data = request.GET

        rooms_clients = str(data["room-clients"]).split("%")[:-1]
        id = int(data['period'])

        period = VacationPackage.objects.get(id=id)
        
        try:
            address_begin = countries[period.origen.countryCode.upper()]
            cities_begin = address_begin[0][list(address_begin[0].keys())[0]]
            address_to = countries[period.room.hotel.location.countryCode.upper()]
            cities_to = address_to[0][list(address_to[0].keys())[0]]
        except:
            address_begin = []
            cities_begin = []
            address_to = []
            cities_to = []
        
        menus = Menu.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)
        
        
        priceTotal = 0.0
        for index,room in enumerate(rooms_clients,start=0):
            clients = room.split("-")
            priceTotal += period.priceTotal(int(clients[0]),int(clients[1]),int(clients[2]))
            rooms_clients[index] = [int(clients[0]),int(clients[1]),int(clients[2])]

        period.priceTotalM = toMoney(priceTotal)
        context = {
            "language":language,
            "strings" : strings,
            "menus" :menus,
            "address_begin" : address_begin,
            "cities_begin" : cities_begin,
            "address_to" : address_to,
            "cities_to" : cities_to,
            "period":period,
            "rooms_clients":rooms_clients

            }
        
        return render(request,'booking_package.html',context)

    def post(self,request,*args,**kwargs):
        data = request.POST
        files = request.FILES



        rooms_clients = str(request.GET["room-clients"]).split("%")[:-1]
        
        dk = date_key()
        bill = Bill.objects.create(code = str(dk[5:]),)
        amount = 0
        revenue = 0

        for r,room in enumerate(rooms_clients,start=1):
            clients = room.split("-")
            adults = int(clients[0])
            children = int(clients[1])
            infants = int(clients[2])

            passagersTypeList = ["Adult",]

            if children > 0 :passagersTypeList.append("Children")
            if infants > 0 :passagersTypeList.append("Infant")
            
            periodPackage = VacationPackage.objects.get(id=int(data["period"]))
            
            n = 1

            _amount = periodPackage.priceTotal(adults,children,infants)
            _revenue = periodPackage.markupValue(adults,children,infants)
            amount += _amount
            revenue += _revenue

            
            if r < 10:_r = f"0{r}"
            else:_r = str(r)
            if n < 10:_n = f"0{n}"
            else:_n = str(n)

            booking = Booking.objects.create(
                user = request.user,
                package = periodPackage,
                amount = _amount,
                markup = _revenue,
                bill = bill,
                reservationCode = dk + _r + _n
            )

            for p in passagersTypeList:
                if p == "Adult" :
                    end = adults + 1
                elif p == "Children" :
                    end = children + 1
                elif p == "Infant" :
                    end = infants + 1


                for i in range(1, end):
                    birthList = data[f'dateBirth-Room{r}-{p}{i}'].split("/")
                    docExpList = data[f'expiration-document-primary-Room{r}-{p}{i}'].split("/")
                    secDocExpList = data[f'expiration-document-secondary-Room{r}-{p}{i}'].split("/")
                    

                    client = Client.objects.create(
                        booking = booking,
                        firstName = data[f'firstName-Room{r}-{p}{i}'].upper(),
                        middleName = data[f'middleName-Room{r}-{p}{i}'].upper(),
                        lastName = data[f'lastName-Room{r}-{p}{i}'].upper(),
                        motherLastName = data[f'motherLastName-Room{r}-{p}{i}'].upper(),
                        birth = date(int(birthList[2]),int(birthList[0]),int(birthList[1])),
                        gender = data[f'gender-Room{r}-{p}{i}'].upper(),
                        
                        documentNumber = data[f'number-document-primary-Room{r}-{p}{i}'],
                        documentExpiration = date(int(docExpList[2]),int(docExpList[0]),int(docExpList[1])),
                        documentType = data[f'type-document-primary-Room{r}-{p}{i}'],
                        documentCountry = data[f'country-document-primary-Room{r}-{p}{i}'],

                        email = data['emailContact'],
                        phone = data['codePhoneNumber'] + data['phoneNumber'],

                        streetBegin = data[f'address-street-1'],
                        cityBegin = data[f'address-city-1'],
                        stateBegin = data[f'address-state-1'],
                    )
                    
                    if f"imagen-document-{p}{i}" in files.keys():
                        image  = files[f"imagen-document-Room{r}-{p}{i}"]
                        imageName = f"primary_document_" + str(client.id) + ".png"
                        client.imageDocument.save(imageName,image)

                    if data[f'number-document-secondary-Room{r}-{p}{i}'] != "" and data[f'expiration-document-secondary-Room{r}-{p}{i}'] != "" and data[f'type-document-secondary-Room{r}-{p}{i}'] != "" and data[f'country-document-secondary-Room{r}-{p}{i}']:
                        client.secondaryDocumentNumber = data[f'number-document-secondary-Room{r}-{p}{i}']
                        client.secondaryDocumentExpiration = date(int(secDocExpList[2]),int(secDocExpList[0]),int(secDocExpList[1]))
                        client.secondaryDocumentType = data[f'type-document-secondary-Room{r}-{p}{i}']
                        client.secondaryDocumentCountry = data[f'country-document-secondary-Room{r}-{p}{i}']
                        client.save()
                        
                        if f"imagen-document-secondary-Room{r}-{p}{i}" in files.keys():
                            image  = files[f"imagen-document-secondary-Room{r}-{p}{i}"]
                            imageName = f"secondary_document_" + str(client.id) + ".png"
                            client.imageSecondaryDocument.save(imageName,image)

            n += 1

        bill.amount = amount
        bill.revenue = revenue
        bill.save()

        return  redirect("reservations")
