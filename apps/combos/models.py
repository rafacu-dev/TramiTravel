from django.db import models

class Combo(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to = 'combo_cuba')
    name = models.CharField(blank = False, null = False,max_length=300)
    details = models.CharField(blank = False, null = False,max_length=300)
    price = models.CharField(blank = False, null = False,max_length=10)
    actived = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.name) 