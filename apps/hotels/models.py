from datetime import datetime
from django.db import models
from apps.reservations.models import Destinatation, Flight

from apps.user.models import UserAccount

class Transport(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank = False, null = False,max_length=300)
    nameCode = models.CharField(blank = False, null = False,max_length=10)
    image = models.ImageField(upload_to = 'package_transport')
    actived = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.name) 

"""class Destinatation(models.Model):
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
        return self.city + ", " + self.country"""

class RoomType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank = False, null = False,max_length=100,unique=True)
    actived = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.name) 

class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to = 'package_hotel')
    name = models.CharField(blank = False, null = False,max_length=300)
    description = models.TextField(blank = True, null = True)


    location = models.ForeignKey(Destinatation,on_delete=models.CASCADE,null=False,blank=False,related_name="location")

    #isForAdults = models.BooleanField(default=True)
    actived = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.name) + " ( " +  str(self.location.name()) + " ) "

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,null=False,blank=False,related_name="hotel")
    quantity = models.IntegerField(default=0,null=False, blank=False)
    room_type = models.ForeignKey(RoomType,on_delete=models.CASCADE,null=False,blank=False,related_name="room_type")

    def __str__(self) -> str:
        return str(self.hotel) + " - " +  str(self.room_type)

class VacationPackage(models.Model):
    id = models.AutoField(primary_key=True)

    room = models.ForeignKey(Room,on_delete=models.CASCADE,null=False,blank=False,related_name="Room")
    
    startDate = models.DateField(null=False)
    lastDate = models.DateField(null=False)

    name = models.CharField(blank = False, null = False,max_length=300)
    description = models.TextField(blank = True, null = True)

    origen = models.ForeignKey(Destinatation,on_delete=models.CASCADE,null=False,blank=False,related_name="origen")

    price_adults_1 = models.FloatField(default=0.0,null=False, blank=False)
    price_adults_2 = models.FloatField(default=0.0,null=False, blank=False)
    price_adults_3 = models.FloatField(null=True, blank=True)
    price_adults_4 = models.FloatField(null=True, blank=True)
    price_adults_5 = models.FloatField(null=True, blank=True)

    price_childrens_1 = models.FloatField(null=True, blank=True)
    price_childrens_2 = models.FloatField(null=True, blank=True)
    price_childrens_3 = models.FloatField(null=True, blank=True)
    price_childrens_4 = models.FloatField(null=True, blank=True)
    price_childrens_5 = models.FloatField(null=True, blank=True)

    price_infants_1 = models.FloatField(null=True, blank=True)
    price_infants_2 = models.FloatField(null=True, blank=True)
    price_infants_3 = models.FloatField(null=True, blank=True)
    price_infants_4 = models.FloatField(null=True, blank=True)
    price_infants_5 = models.FloatField(null=True, blank=True)

    taxes = models.FloatField(default=0.0,null=False, blank=False)
    flight = models.FloatField(default=0.0,null=False, blank=False)
    transfer = models.FloatField(default=0.0,null=False, blank=False)
    markup = models.FloatField(default=0.0,null=False, blank=False) # Se da en %

        
    #servicesInclude = models.CharField(blank = True, null = True,max_length=100)    
    #accommodation = models.CharField(blank = True, null = True,max_length=100)

    flightBegin = models.ForeignKey(Flight,on_delete=models.SET_NULL,null=True,blank=True,related_name="FlightBegin")
    flightReturn = models.ForeignKey(Flight,on_delete=models.SET_NULL,null=True,blank=True,related_name="FlightReturn")
    
    transport = models.ForeignKey(Transport,on_delete=models.CASCADE,null=True,blank=True)
    departure_traslate = models.DateTimeField(blank = True, null = True)
    arrival_traslate = models.DateTimeField(blank = True, null = True)
    departure_traslate_return = models.DateTimeField(blank = True, null = True)
    arrival_traslate_return = models.DateTimeField(blank = True, null = True)
    
    actived = models.BooleanField(default=True)

    def maxAdults(self) -> int:
        if self.price_adults_2 == None: return 1
        if self.price_adults_3 == None: return 2
        if self.price_adults_4 == None: return 3
        if self.price_adults_5 == None: return 4
        return 5
    
    def maxChildrens(self) -> int:
        if self.price_childrens_1 == None: return 0
        if self.price_childrens_2 == None: return 1
        if self.price_childrens_3 == None: return 2
        if self.price_childrens_4 == None: return 3
        if self.price_childrens_5 == None: return 4
        return 5
    
    def maxInfants(self) -> int:
        if self.price_infants_1 == None: return 0
        if self.price_infants_2 == None: return 1
        if self.price_infants_3 == None: return 2
        if self.price_infants_4 == None: return 3
        if self.price_infants_5 == None: return 4
        return 5    

    def numberNights(self) -> str:
        return (self.lastDate - self.startDate).days
    
    def pricePackage(self,adults,childrens,infants) -> float:
        amount = 0.0

        if adults >= 5: amount += ((self.price_adults_2 * 2) + self.price_adults_3 + self.price_adults_4 + (self.price_adults_5 * adults - 4))
        elif adults == 4: amount += ((self.price_adults_2 * 2) + self.price_adults_3 + self.price_adults_4)
        elif adults == 3 :  amount += ((self.price_adults_2 * 2) + self.price_adults_3)
        elif adults == 2:  amount += (self.price_adults_2 * 2)
        else:  amount += self.price_adults_1
        
        if childrens >= 5: amount += ((self.price_childrens_2 * 2) + self.price_childrens_3 + self.price_childrens_4 + (self.price_childrens_5 * childrens - 4))
        elif childrens == 4: amount += ((self.price_childrens_2 * 2) + self.price_childrens_3 + self.price_childrens_4)
        elif childrens == 3 :  amount += ((self.price_childrens_2 * 2) + self.price_childrens_3)
        elif childrens == 2:  amount += (self.price_childrens_2 * 2)
        elif childrens == 1:  amount += self.price_childrens_1

        if infants >= 5: amount += ((self.price_infants_2 * 2) + self.price_infants_3 + self.price_infants_4 + (self.price_infants_5 * infants - 4))
        elif infants == 4: amount += ((self.price_infants_2 * 2) + self.price_infants_3 + self.price_infants_4)
        elif infants == 3 :  amount += ((self.price_infants_2 * 2) + self.price_infants_3)
        elif infants == 2:  amount += (self.price_infants_2 * 2)
        elif infants == 1:  amount += self.price_infants_1

        return amount
    
    def priceTotal(self,adults,childrens,infants) -> float:
        price = (self.pricePackage(adults,childrens,infants) * self.numberNights()) + (self.flight * (adults + childrens)) + (self.transfer * (adults + childrens))
        markup = price * self.markup / 100 
        return price + (self.taxes *(adults+childrens+infants))+ markup
        
    def markupValue(self,adults,childrens,infants) -> float:
        price = (self.pricePackage(adults,childrens,infants) * self.numberNights()) + (self.flight * (adults + childrens)) + (self.transfer * (adults + childrens))
        markup = price * self.markup / 100 
        return markup

class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(blank = False, null = False, max_length=10)
    zelle = models.CharField(blank = True, null = True, max_length=100)  
    zelle_owner = models.CharField(blank = True, null = True, max_length=100)  
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(blank = True, null = True, default= None)     
    
    amount = models.FloatField(blank=False, null=False,default=0)
    revenue = models.FloatField(blank=False, null=False,default=0)    
    liquidated = models.FloatField(blank=False, null=False,default=0)

    liquidated = models.FloatField(blank=False, null=False,default=0)

    def __str__(self) -> str:
        return str(self.code)
    
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

    def amountMoney(self) -> str:
        amount = self.amount + self.revenue
        if len(str(amount).split(".")[1]) == 1: return "$ " + str(amount) + "0"
        return "$ " + str(amount)
    

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserAccount,on_delete=models.CASCADE,null=False,blank=False,related_name="user_account")
    package = models.ForeignKey(VacationPackage,on_delete=models.SET_NULL,null=True,blank=True,related_name="VacationPackage")
    date = models.DateTimeField(auto_now_add=True)

    reservationCode = models.BigIntegerField(blank = False, null = False)
    pnr = models.CharField(blank = True, null = True, max_length=50)
    pnr_return = models.CharField(blank = True, null = True, max_length=50)
    
    bill = models.ForeignKey(Bill,on_delete=models.CASCADE,null=False,blank=False,related_name="hotels_bill")
    
    amount = models.FloatField(blank=False, null=False,default=0)
    markup = models.FloatField(blank=False, null=False,default=0)
    liquidated = models.FloatField(blank=False, null=False,default=0)
  
    actived = models.BooleanField(default=True)

    def holder(self):
        return Client.objects.filter(booking=self)[0].__str__()

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE,null=False,blank=False,related_name="booking")
    firstName = models.CharField(blank = False, null = False, max_length=100)
    middleName = models.CharField(blank = True, null = True,max_length=100)
    lastName = models.CharField(blank = False, null = False, max_length=100)
    motherLastName = models.CharField(blank = True, null = True,max_length=100)
    birth = models.DateField(blank = False, null = False)
    gender = models.CharField(blank = False, null = False, max_length=1)

    email = models.EmailField(blank = False, null = False)
    phone = models.CharField(blank = False, null = False, max_length=20)

    imageDocument = models.ImageField(upload_to = 'package-booking-document', blank=True, null=True)
    documentNumber = models.CharField(blank = False, null = False, max_length=14)
    documentExpiration = models.DateField(blank = False, null = False)
    documentType = models.CharField(blank = False, null = False, max_length=50)
    documentCountry = models.CharField(blank = False, null = False, max_length=50)

    imageSecondaryDocument = models.ImageField(upload_to = 'package-booking-document', blank=True, null=True)
    secondaryDocumentNumber = models.CharField(blank = True, null = True, max_length=14)
    secondaryDocumentExpiration = models.DateField(blank = True, null = True)
    secondaryDocumentType = models.CharField(blank = True, null = True, max_length=50)
    secondaryDocumentCountry = models.CharField(blank = True, null = True, max_length=50)

    streetBegin = models.CharField(blank = False, null = False, max_length=200)
    cityBegin = models.CharField(blank = False, null = False, max_length=100)
    stateBegin = models.CharField(blank = False, null = False, max_length=100)

    def __str__(self) -> str:
        return self.lastName + " " + self.motherLastName + ", " + self.firstName + " " + self.middleName
    
"""
Total = (Hotel * Nights) + Taxes + Flight + Transfer + Markup +- Additional Fee/Discount

Markup = ((Hotel * Nights) + Flight + Transfer) / (1 - (Markup Percentage / 100))

Hotel for Adults:

1 Pax = 1rst Price
2 Pax = 2nd Price * 2
3 Pax = 2nd Price * 2 + 3rd Price
4 Pax = 2nd Price * 2 + 3rd Price + 4th Price
5 Pax and more = 2nd Price * 2 + 3rd Price + 4th Price + (5th Price  PaxCount - 4)
"""