from django.db import models

# Create your models here.

class Pasms(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(blank = False, null = False,max_length=10,unique=True)
    case = models.CharField(max_length=15)
    date = models.DateField(null=True)