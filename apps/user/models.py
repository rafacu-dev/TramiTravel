from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
import random


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class Agency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank = False, null = False,max_length=300)
    logo = models.ImageField(blank = True, null = True,upload_to = 'agency')
    address = models.CharField(blank = False, null = False, max_length=200)
    email = models.EmailField(max_length=255, blank = False, null = False)
    phone = models.CharField(blank = False, null = False, max_length=20)
    fax = models.CharField(blank = False, null = False, max_length=20)
    fei_ein_number = models.CharField(blank = False, null = False, max_length=20)
    seller_travel_number = models.CharField(blank = False, null = False, max_length=20)


    contact_name = models.CharField(blank = False, null = False,max_length=300)
    contact_email = models.EmailField(max_length=255, blank = False, null = False)
    contact_phone = models.CharField(blank = False, null = False, max_length=20)

    revenue = models.FloatField(blank=False, null=False,default=10.0)
    license = models.FileField(null=True, blank=True, upload_to = 'agency-license')

    credit = models.FloatField(blank=False, null=False,default=0)

    actived = models.BooleanField(default=True)

    def amountMoney(self) -> str:
        amount = self.revenue
        if len(str(amount).split(".")[1]) == 1: return "$ " + str(amount) + "0"
        return "$ " + str(amount)

    def creditMoney(self) -> str:
        credit = self.credit
        if len(str(credit).split(".")[1]) == 1: return "$ " + str(credit) + "0"
        return "$ " + str(credit)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    #user = models.CharField(max_length=100, blank = False, null = False, unique=True)
    email = models.EmailField(max_length=255, blank = True, null = True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    agency = models.ForeignKey(Agency,on_delete=models.CASCADE,null=True,blank=True,related_name="agency")
    is_admin_agency = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj = None):
        return True

    def has_mmodule_perms(self,app_label):
        return True


class ConfirmCode(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, blank = True, null = True, unique=True)
    code = models.CharField(blank = False, null = False, max_length=5)
    failures = models.IntegerField(blank = False, null = False,default=0)
    date_time = models.DateTimeField(null=False, auto_now_add=True)

    

class RecreatePassword(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserAccount,on_delete=models.CASCADE,null=False,blank=False)
    password = models.TextField(blank = False, null = False)
    code = models.CharField(blank = False, null = False, max_length=5)
    failures = models.IntegerField(blank = False, null = False,default=0)
    date_time = models.DateTimeField(null=False, auto_now_add=True)



class CreditRecharge(models.Model):
    id = models.AutoField(primary_key=True)
    zelle = models.CharField(blank = True, null = True, max_length=100)  
    zelle_owner = models.CharField(blank = True, null = True, max_length=100)  
    date = models.DateTimeField(auto_now_add=True)
    agency = models.ForeignKey(Agency,on_delete=models.CASCADE,null=True,blank=True,related_name="agency_credit_recharge")
    user = models.ForeignKey(UserAccount,on_delete=models.SET_NULL,null=True,blank=True,related_name="user_account_credit_recharge")
    amount = models.FloatField(blank=False, null=False,default=0)
    amount_confirmed = models.FloatField(blank=False, null=False,default=0)
    confirm = models.BooleanField(blank = True, null = True, default= None) 