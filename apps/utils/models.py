from django.db import models

from apps.user.models import UserAccount


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserAccount,on_delete=models.CASCADE,null=False,blank=False)
    product = models.CharField(blank = False, null = False, max_length=200)
    code = models.CharField(blank = False, null = False, max_length=10)
    zelle = models.CharField(blank = True, null = True, max_length=100)  
    zelle_owner = models.CharField(blank = True, null = True, max_length=100)  
    date = models.DateTimeField(auto_now_add=True)
    ammount = models.FloatField(blank=False, null=False,default=0)
    paid = models.BooleanField(blank = True, null = True, default= None)
