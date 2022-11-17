from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
#JWT token
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', Register.as_view(), name="register"),
    path('myadvertisement/', MyAdvertisement.as_view(), name="createadv"),
    path('myvehicle/', MyVehicle.as_view(), name="myvehicle"),
    path('viewadvertisement/', ViewAdvertisement.as_view(), name="viewadvertisement"),

]
