import calendar
from datetime import date, datetime
from apps.utils.countries import countries
from django.shortcuts import redirect, render
from django.views.generic import View
from apps.hotels.models import Bill, Booking, Destinatation, Hotel, RoomType, VacationPackage

from apps.menus.models import Menu
from apps.utils.utils import toMoney
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


class Hotels(View):
    def test_user(self):
        return self.request.user.is_authenticated and self.request.user.agencie
    
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
    

    
class ReservationsView(View):
    def get(self,request,*args,**kwargs):
        data = request.GET
        menus = Menu.objects.filter(actived=True).order_by('position')
        strings,language = get_strings(request.COOKIES)

        reservations = Booking.objects.filter(user = request.user)
        
        
        context = {
            "language":language,
            "strings" : strings,
            "menus" :menus,
            "reservations":reservations
            }
        
        return render(request,'reservations_package.html',context)
    
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

            _amount = periodPackage.pricePackage(adults,children,infants)
            _revenue = periodPackage.markupValue(adults,children,infants)
            amount += _amount
            revenue += _revenue


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
                    
                    if n < 10:_n = f"0{n}"
                    else:_n = str(n)

                    booking = Booking.objects.create(
                        user = request.user,
                        package = periodPackage,

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

                        amount = _amount,
                        markup = _revenue,

                        bill = bill,

                        reservationCode = dk + _n + "01"
                    )
                    
                    if f"license-{p}{i}" in files.keys():
                        booking.license = data[f'license-Room{r}-{p}{i}']
                        booking.save()
                    
                    if f"imagen-document-{p}{i}" in files.keys():
                        image  = files[f"imagen-document-Room{r}-{p}{i}"]
                        imageName = f"primary_document_" + str(booking.id) + ".png"
                        booking.imageDocument.save(imageName,image)

                    if data[f'number-document-secondary-Room{r}-{p}{i}'] != "" and data[f'expiration-document-secondary-Room{r}-{p}{i}'] != "" and data[f'type-document-secondary-Room{r}-{p}{i}'] != "" and data[f'country-document-secondary-Room{r}-{p}{i}']:
                        booking.secondaryDocumentNumber = data[f'number-document-secondary-Room{r}-{p}{i}']
                        booking.secondaryDocumentExpiration = date(int(secDocExpList[2]),int(secDocExpList[0]),int(secDocExpList[1]))
                        booking.secondaryDocumentType = data[f'type-document-secondary-Room{r}-{p}{i}']
                        booking.secondaryDocumentCountry = data[f'country-document-secondary-Room{r}-{p}{i}']
                        booking.save()
                        
                        if f"imagen-document-secondary-Room{r}-{p}{i}" in files.keys():
                            image  = files[f"imagen-document-secondary-Room{r}-{p}{i}"]
                            imageName = f"secondary_document_" + str(booking.id) + ".png"
                            booking.imageSecondaryDocument.save(imageName,image)

                    n += 1

        bill.amount = amount
        bill.revenue = revenue
        bill.save()

        return  redirect("reservations")
