from rest_framework import serializers
from .models import *


class GetAdvertisementSerializers(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()
    price_per_km = serializers.CharField()
    vehicle_id = serializers.CharField()

    class Meta:
        model = Advertisement
        fields = (
            'title',
            'description',
            'price_per_km',
            'vehicle_id'
        )


class ViewVehicleSerializers(serializers.ModelSerializer):
    brand = serializers.CharField()
    model = serializers.CharField()
    number_plate = serializers.CharField()
    id = serializers.CharField()

    class Meta:
        model = Vehicle
        fields = (
            'brand',
            'model',
            'number_plate',
            'id'
        )


class ViewAdvertisementSerializers(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    datetime = serializers.SerializerMethodField('get_date')
    brand = serializers.SerializerMethodField('get_brand')
    model = serializers.SerializerMethodField('get_model')

    class Meta:
        model = Advertisement
        fields = (
            'title',
            'description',
            'price_per_km',
            'id',
            'name',
            'datetime',
            'brand',
            'model'
        )

    @staticmethod
    def get_name(obj):
        user_id = obj.user_id
        profile = User.objects.filter(id=user_id).first()
        f_name = profile.first_name
        l_name = profile.last_name
        name = f_name + " " + l_name
        return name

    @staticmethod
    def get_date(obj):
        date = obj.datetime
        return date.strftime("%d" + " " + "%b" + " " + "%y")

    @staticmethod
    def get_brand(obj):
        vehicle = Vehicle.objects.filter(id=obj.vehicle_id).first()
        brand = vehicle.brand
        model = vehicle.model
        return brand

    @staticmethod
    def get_model(obj):
        vehicle = Vehicle.objects.filter(id=obj.vehicle_id).first()
        model = vehicle.model
        return model

