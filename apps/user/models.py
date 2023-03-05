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

#User = settings.AUTH_USER_MODEL


class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    #user = models.CharField(max_length=100, blank = False, null = False, unique=True)
    email = models.EmailField(max_length=255, blank = True, null = True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

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
