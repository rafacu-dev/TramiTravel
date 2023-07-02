
from datetime import time,datetime, timedelta

from django.db import models

from apps.user.models import UserAccount

from .validators import validate_file_extension

# Create your models here.

class ClassType(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.IntegerField(null=False,blank=False)
    name_es = models.CharField(blank = False, null = False,max_length=100)
    name_en = models.CharField(blank = False, null = False,max_length=100)
    css = models.TextField(blank = True, null = True)
    actived = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.name_es
    """
    background-image: linear-gradient(to bottom, #FF5F6D, #FFC371);color: white;
    /* Nota: En este ejemplo, el gradiente va desde el color rojo (#FF5F6D) hasta el color naranja (#FFC371) */
    
    padding: 10px 20px;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.25);
    """

class Destinatation(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(blank = False, null = False,max_length=300)
    country = models.CharField(blank = False, null = False,max_length=300)
    cityCode = models.CharField(blank = False, null = False,max_length=3)
    countryCode = models.CharField(blank = False, null = False,max_length=3)
    begin = models.BooleanField(default=True,blank=False,null=False)
    destination = models.BooleanField(default=True,blank=False,null=False)
    actived = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.city + ", " + self.country
        
    def name(self) -> str:
        return self.city + ", " + self.country

class Airline(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank = False, null = False,max_length=300)
    nameCode = models.CharField(blank = False, null = False,max_length=10)
    image = models.ImageField(upload_to = 'airline')

    actived = models.BooleanField(default=True)
    #baggagePolicy = models.FileField(null=True, blank=True, upload_to = 'baggage-policy', validators=[validate_file_extension])

    def __str__(self) -> str:
        return self.name

class BaggagePolicy(models.Model):
    id = models.AutoField(primary_key=True)
    identifier = models.CharField(blank = False, null = False,max_length=100)
    baggagePolicy = models.FileField(null=True, blank=True, upload_to = 'baggage-policy', validators=[validate_file_extension])
    actived = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.identifier

class Charter(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank = False, null = False,max_length=300)
    image = models.ImageField(upload_to = 'charter')
    url = models.URLField(blank = True, null = True)

    actived = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class Aircraft(models.Model):
    id = models.AutoField(primary_key=True)
    make = models.CharField(blank = False, null = False, max_length=50)
    model = models.CharField(blank = False, null = False, max_length=50)
    carrier_code = models.ForeignKey(Airline,on_delete=models.CASCADE,null=False,blank=False)
    pax_seats = models.IntegerField(blank = False, null = False)
    first_class_seats = models.IntegerField(blank = False, null = False)

    actived = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.model + " - " + self.carrier_code.__str__()

class Flight(models.Model):
    id = models.AutoField(primary_key=True)

    begin = models.ForeignKey(Destinatation,on_delete=models.CASCADE,null=False,blank=False,related_name="From")
    to = models.ForeignKey(Destinatation,on_delete=models.CASCADE,null=False,blank=False,related_name="To")
    
    gate = models.CharField(blank = False, null = False,max_length=20)

    charter = models.ForeignKey(Charter,on_delete=models.CASCADE,null=True,blank=True)
    
    aircraft = models.ForeignKey(Aircraft,on_delete=models.CASCADE,null=False,blank=False)
    number = models.CharField(blank = False, null = False,max_length=5)
    
    checkinMoment = models.IntegerField(default=4,null=False,blank=False)

    departure = models.TimeField(null=False)
    arrival = models.TimeField(null=False)

    
    date = models.DateField(null=False)
    
    ability = models.IntegerField(default=1 ,null=False, blank=False)

    priceAdult = models.FloatField(blank=False, null=False)
    revenueAdult = models.FloatField(blank=False, null=False)

    priceChildren = models.FloatField(blank=False, null=False)
    revenueChildren = models.FloatField(blank=False, null=False)

    priceInfant = models.FloatField(blank=False, null=False)
    revenueInfant = models.FloatField(blank=False, null=False)

    agencyCommission = models.FloatField(blank=False, null=False,default=10.0)

    class_type = models.ForeignKey(ClassType,on_delete=models.CASCADE,null=False,blank=False,related_name="class_type")
    
    baggagePolicy = models.ForeignKey(BaggagePolicy,on_delete=models.SET_NULL,null=True,blank=True,related_name="baggage_policy")

    packagesOnly = models.BooleanField(default=False)

    actived = models.BooleanField(default=True)

    def __str__(self) -> str:
        t = f"{self.date} / {self.begin} - {self.to} "
        if self.charter:  t += f"/  {self.charter.name}"
        return t
    
    def date_en(self):
        return self.date.strftime("%A, %b %d")
    
    def departureMS(self):
        departure_time = datetime.combine(self.date, self.departure)
        milisegundos = int(departure_time.timestamp() * 1000)
        return milisegundos
    
    def arrivalMS(self):
        
        arrival_time = datetime.combine(self.date, self.arrival)
        departure_time = datetime.combine(self.date, self.departure)
        if arrival_time < departure_time:
            arrival_time += timedelta(days=1)
        milisegundos = int(arrival_time.timestamp() * 1000)
        return milisegundos

    def checkin(self) -> time:
        hour = self.departure.hour
        checkinHour = hour - self.checkinMoment
        
        if checkinHour <0: checkinHour = 24 + checkinHour

        return time(checkinHour,self.departure.minute,self.departure.second)

    def duration(self) -> str:
        departure = self.departure.hour * 60 + self.departure.minute
        arrival = self.arrival.hour * 60 + self.arrival.minute

        if departure > arrival: 
            duration = 1440 - departure + arrival
        else: 
            duration = arrival - departure

        if duration < 60: 
            if duration < 10:duration = f"0{duration}"            
            return f"00 h  {duration} min"

        elif duration % 60 == 0:
            if duration // 60 < 10:
                h = "0" + str(duration // 60)
            else:
                h = str(duration // 60)
                
            return h + "  h 00 min"

        if duration // 60 < 10:
            h = "0" + str(duration // 60)
        else:
            h = str(duration // 60)

        if duration % 60 < 10:
            m = "0" + str(duration % 60)
        else:
            m = str(duration % 60)

        return h + " h  " + m + " min"
    
    def priceMoney(self) -> str:
        price = self.priceAdult + self.revenueAdult
        if len(str(price).split(".")[1]) == 1: return "$ " + str(price) + "0"
        return "$ " + str(price)
    
    def priceAgencyMoney(self,revenue_agency) -> str:
        price = 0.0
        if self.priceAdult > 0.0:price = self.priceAdult + self.agencyCommission + revenue_agency
        if len(str(price).split(".")[1]) == 1: return "$ " + str(price) + "0"
        return "$ " + str(price)
    
    def adultAgencyCommission(self) -> float:
        if self.priceAdult > 0.0:return self.priceInfant + self.agencyCommission
        return self.priceAdult
    
    def adultChildrenCommission(self) -> float:
        if self.priceChildren > 0.0:return self.priceInfant + self.agencyCommission
        return self.priceChildren
    
    def adultInfantCommission(self) -> float:
        if self.priceInfant > 0.0:return self.priceInfant + self.agencyCommission
        return self.priceInfant
    
    def capacity(self) -> int:
        bookings = Booking.objects.filter(flight = self).count()
        return self.ability - bookings

class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(blank = False, null = False, max_length=10)
    zelle = models.CharField(blank = True, null = True, max_length=100)  
    zelle_owner = models.CharField(blank = True, null = True, max_length=100)  
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(blank = True, null = True, default= None) 

    liquidated = models.FloatField(blank=False, null=False,default=0)

    def __str__(self) -> str:
        return str(self.code)

    def amount(self) -> float:
        amount = 0
        bookings = Booking.objects.filter(bill = self)

        for booking in bookings:
            amount += booking.amount
        return amount

    def revenue(self) -> float:
        revenue = 0
        bookings = Booking.objects.filter(bill = self)

        for booking in bookings:
            revenue += booking.revenue

        return revenue
    
    def amountMoney(self) -> str:
        amount = self.amount() + self.revenue()
        if len(str(amount).split(".")[1]) == 1: return "$ " + str(amount) + "0"
        return "$ " + str(amount)
    
    def hoursRest(self) -> list:
        dt_tuple = datetime.now().timetuple()
        moment = (dt_tuple.tm_hour * 60 * 60) + (dt_tuple.tm_min * 60) + dt_tuple.tm_sec
        momentCreated = (self.date.hour * 60 * 60) + (self.date.minute * 60) + self.date.second


        if moment > momentCreated:
            moment = 86400 - moment + momentCreated
        else:
            moment = 86400 - momentCreated

        hour = moment // 3600
        
        listReturn = [hour,]

        if hour < 10:
            listReturn += [0,hour]
        else:
            _hour = str(hour)
            listReturn += [_hour[0],_hour[1]]
        
        return listReturn
    
    def minutesRest(self) -> list:
        dt_tuple = datetime.now().timetuple()

        moment = (dt_tuple.tm_hour * 60 * 60) + (dt_tuple.tm_min * 60) + dt_tuple.tm_sec
        momentCreated = (self.date.hour * 60 * 60) + (self.date.minute * 60) + self.date.second


        if moment > momentCreated:
            moment = 86400 - moment + momentCreated
        else:
            moment = 86400 - momentCreated

        hour = moment // 3600
        min = (moment - (hour * 3600)) // 60
        
        listReturn = [min,]

        if min < 10:
            listReturn += [0,min]
        else:
            _min = str(min)
            listReturn += [_min[0],_min[1]]
        return listReturn

    def secondsRest(self) -> list:
        dt_tuple = datetime.now().timetuple()
        moment = (dt_tuple.tm_hour * 60 * 60) + (dt_tuple.tm_min * 60) + dt_tuple.tm_sec
        momentCreated = (self.date.hour * 60 * 60) + (self.date.minute * 60) + self.date.second


        if moment > momentCreated:
            moment = 86400 - moment + momentCreated
        else:
            moment = 86400 - momentCreated

        hour = moment // 3600
        min = (moment - (hour * 3600)) // 60
        sec = moment - (hour * 3600) - (min * 60)
        
        listReturn = [sec,]

        if sec < 10:
            listReturn += [0,sec]
        else:
            _sec = str(sec)
            listReturn += [_sec[0],_sec[1]]
        return listReturn

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserAccount,on_delete=models.CASCADE,null=False,blank=False,related_name="user")
    flight = models.ForeignKey(Flight,on_delete=models.SET_NULL,null=True,blank=True,related_name="booking")
    date = models.DateField(auto_now_add=True)
    
    firstName = models.CharField(blank = False, null = False, max_length=100)
    middleName = models.CharField(blank = True, null = True,max_length=100)
    lastName = models.CharField(blank = False, null = False, max_length=100)
    motherLastName = models.CharField(blank = True, null = True,max_length=100)
    birth = models.DateField(blank = False, null = False)
    gender = models.CharField(blank = False, null = False, max_length=1)

    email = models.EmailField(blank = False, null = False)
    phone = models.CharField(blank = False, null = False, max_length=20)

    imageDocument = models.ImageField(upload_to = 'booking-document', blank=True, null=True)
    documentNumber = models.CharField(blank = False, null = False, max_length=14)
    documentExpiration = models.DateField(blank = False, null = False)
    documentType = models.CharField(blank = False, null = False, max_length=50)
    documentCountry = models.CharField(blank = False, null = False, max_length=50)

    imageSecondaryDocument = models.ImageField(upload_to = 'booking-document', blank=True, null=True)
    secondaryDocumentNumber = models.CharField(blank = True, null = True, max_length=14)
    secondaryDocumentExpiration = models.DateField(blank = True, null = True)
    secondaryDocumentType = models.CharField(blank = True, null = True, max_length=50)
    secondaryDocumentCountry = models.CharField(blank = True, null = True, max_length=50)

    streetBegin = models.CharField(blank = False, null = False, max_length=200)
    cityBegin = models.CharField(blank = False, null = False, max_length=100)
    stateBegin = models.CharField(blank = False, null = False, max_length=100)

    streetTo = models.CharField(blank = False, null = False, max_length=200)
    cityTo = models.CharField(blank = False, null = False, max_length=100)
    stateTo = models.CharField(blank = False, null = False, max_length=100)

    reservationCode = models.BigIntegerField(blank = False, null = False)
    pnr = models.CharField(blank = True, null = True, max_length=50)
    
    amount = models.FloatField(blank=False, null=False,default=0)
    revenue = models.FloatField(blank=False, null=False,default=0)
    liquidated = models.FloatField(blank=False, null=False,default=0)

    license = models.CharField(blank = True, null = True, max_length=100)
    
    bill = models.ForeignKey(Bill,on_delete=models.CASCADE,null=False,blank=False,related_name="bill")
  
    actived = models.BooleanField(default=True)

    
    def isReturn(self) -> bool:
        if str(self.reservationCode)[-1] == "2": return True
        return False
        
    def reservationCodeGroup(self) -> str:
        return str(self.reservationCode)[:-2]
        
    def name(self) -> str:
        return self.lastName + " " + self.motherLastName + ", " + self.firstName + " " + self.middleName

    def amountAgencieMoney(self,revenue_agency) -> str:
        amount = self.amount + self.flight.agencyCommission + revenue_agency
        if len(str(amount).split(".")[1]) == 1: return "$ " + str(amount) + "0"
        return "$ " + str(amount)
    
    def amountMoney(self) -> str:  #-- Solo para agencias
        amount = self.amount + self.flight.agencyCommission
        if len(str(amount).split(".")[1]) == 1: return "$ " + str(amount) + "0"
        return "$ " + str(amount)
    
    def liquidatedMoney(self) -> str:
        amount = self.liquidated
        if len(str(amount).split(".")[1]) == 1: return "$ " + str(amount) + "0"
        return "$ " + str(amount)

