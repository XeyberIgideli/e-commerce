from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager,)
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.core.mail import send_mail
import uuid 
# Create your models here.

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user



class Customer (AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255) 
    
    # User status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name'] 
     
    objects = CustomAccountManager()
    
    
    def send_email (self, subject, message):
        return send_mail(
            subject,
            message,
            "d@gmail.com",
            [self.email],
            fail_silently=False
        )
    
    def __str__ (self):
        return self.email    
        

class Address (models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)        
    customer = models.ForeignKey(Customer, verbose_name= "Customer", on_delete=models.CASCADE)
    fullname = models.CharField(max_length=155, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    delivery_instructions = models.CharField(max_length=255, blank=True)
    address_line_1 = models.CharField(max_length=155, blank=True)
    address_line_2 = models.CharField(max_length=155, blank=True)
    town_city = models.CharField(max_length=155, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    default = models.BooleanField(_("Default"), default=False)
    
    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        
    def __str__(self) -> str:
        return self.id    