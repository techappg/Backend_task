from django.contrib import admin
from .models import *
# Register your models here.

myModels = [User, Advertisement, Vehicle]
admin.site.register(myModels)