from django.db import models



class Location(models.Model):
    id = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    androidId = models.CharField(max_length=200,null=False,blank=False)
    date = models.DateField(auto_now_add=True)