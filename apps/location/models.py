from django.db import models



class Location(models.Model):
    id = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    androidId = models.CharField(max_length=200,null=False,blank=False)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.date)
    



class GetRequests(models.Model):
    id = models.AutoField(primary_key=True)
    ip_address = models.CharField(max_length=100,null=False,blank=False)
    concurrence = models.IntegerField(default=0,null=False,blank=False)
    last_use = models.DateTimeField(auto_now_add=True)