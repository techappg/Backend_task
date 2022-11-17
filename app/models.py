from django.db import models
from django.db.models import ForeignKey
from django.db.models.fields import *
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    address = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    age = models.CharField(max_length=50, blank=True, null=True)


class Vehicle(models.Model):
    user = ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_vehicle")
    brand = CharField(max_length=50, blank=True, null=True)
    model = CharField(max_length=50, blank=True, null=True)
    number_plate = CharField(max_length=50, blank=True, null=True)


class Advertisement(models.Model):
    vehicle = ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    user = ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_adv")
    title = CharField(max_length=50, blank=True, null=True)
    description = CharField(max_length=50, blank=True, null=True)
    price_per_km = CharField(max_length=50, blank=True, null=True)
    datetime = DateTimeField(blank=False, null=True)



