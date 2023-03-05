from django.db import models

from apps.user.models import UserAccount

class Refill(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserAccount,on_delete=models.CASCADE,null=False,blank=False)
    date = models.DateTimeField(auto_now_add=True)

    code = models.CharField(blank = False, null = False, max_length=10)

    emailZelle = models.CharField(blank = True, null = True, max_length=100)
    userZelle = models.CharField(blank = True, null = True, max_length=100)  

    deposit = models.FloatField(blank=False, null=False)
    receiver = models.FloatField(blank=False, null=False)

    card = models.IntegerField()
    receivingPerson = models.CharField(blank = False, null = False, max_length=150)

    status = models.BooleanField(blank=True, null=True, default= None)

    def __str__(self) -> str:
        return f"{self.user} - {self.code}"
    
    
    def depositMoney(self) -> str:
        if len(str(self.deposit).split(".")[1]) == 1: return "$ " + str(self.deposit) + "0"
        return "$ " + str(self.deposit)
        
    def receiverMoney(self) -> str:
        if len(str(self.receiver).split(".")[1]) == 1: return "$ " + str(self.receiver) + "0"
        return "$ " + str(self.receiver)


class Config(models.Model):
    id = models.AutoField(primary_key=True)
    clave = models.CharField(max_length=300, blank = False, null = False, unique=True)
    valor = models.CharField(max_length=300, blank = False, null = False)
