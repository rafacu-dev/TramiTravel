from django.db import models
from ckeditor.fields import RichTextField

from .validators import validate_tag


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.IntegerField(unique=True,null=False,blank=False)
    tag = models.CharField(unique=True,blank = False, null = False, max_length=50,validators=[validate_tag])
    
    name_es = models.CharField(max_length=200,null=False,blank=False)
    name_en = models.CharField(max_length=200,null=False,blank=False)

    actived = models.BooleanField(default=True)

    def seccions(self) -> list:
        return Seccion.objects.filter(menu=self).order_by('position')
        
    def necessary(self) -> bool:
        return Seccion.objects.filter(menu=self).exists()

    def __str__(self) -> str:
        return str(self.tag)

class Seccion(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(unique=True,blank = False, null = False, max_length=50,validators=[validate_tag])
    position = models.IntegerField(null=False,blank=False)
    menu = models.ForeignKey(Menu,on_delete=models.CASCADE,null=False,blank=False,related_name="Menu")
    
    image = models.ImageField(blank = False, null = False,upload_to = 'seccion')
    
    name_es = models.CharField(max_length=200,null=False,blank=False)
    name_en = models.CharField(max_length=200,null=False,blank=False)

    smallDescription_es = models.TextField(null=True,blank=True)
    smallDescription_en = models.TextField(null=True,blank=True)

    description_es = models.TextField(null=True,blank=True)
    description_en = models.TextField(null=True,blank=True)

    form = models.TextField(null=True,blank=True)

    actived = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.tag


class OfertGroup(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.IntegerField(unique=True,null=False,blank=False)
    tag = models.CharField(unique=True,blank = False, null = False, max_length=50,validators=[validate_tag])

    name_es =models.CharField(max_length=200,null=False,blank=False)
    name_en =models.CharField(max_length=200,null=False,blank=False)

    comment_es = models.CharField(max_length=200,null=False,blank=False)
    comment_en = models.CharField(max_length=200,null=False,blank=False)

    actived = models.BooleanField(default=True)

    def getOferts(self) -> list:
        return Ofert.objects.filter(ofertGroup=self).order_by('position')
        
    def necessary(self) -> bool:
        return Ofert.objects.filter(ofertGroup=self).exists()

    def __str__(self) -> str:
        return str(self.tag)
        

class Ofert(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(unique=True,blank = False, null = False, max_length=50,validators=[validate_tag])
    position = models.IntegerField(null=False,blank=False)
    ofertGroup = models.ForeignKey(OfertGroup,on_delete=models.CASCADE,null=False,blank=False,related_name="OfertGroup")
    
    image = models.ImageField(blank = False, null = False,upload_to = 'ofert')
    image2 = models.ImageField(blank = True, null = True,upload_to = 'ofert')
    image3 = models.ImageField(blank = True, null = True,upload_to = 'ofert')

    name_es =models.CharField(max_length=200,null=False,blank=False)
    name_en =models.CharField(max_length=200,null=False,blank=False)
    
    description_es = models.TextField(null=False,blank=False)
    description_en = models.TextField(null=False,blank=False)
    message_es = models.TextField(null=False,blank=False)
    message_en = models.TextField(null=False,blank=False)

    actived = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.tag

