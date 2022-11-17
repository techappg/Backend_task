from datetime import datetime
from http import HTTPStatus

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import *
import traceback
from .serializers import *


class Register(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            body_data = request.data
            f_name = body_data['f_name']
            l_name = body_data['l_name']
            age = body_data['age']
            address = body_data['address']
            street = body_data['street']
            city = body_data['city']
            country = body_data['country']
            number_plate = body_data['number_plate']
            model = body_data['model']
            brand = body_data['brand']
            email_id = body_data['email_id']
            password = body_data['password']

            if number_plate and model and brand:
                user_id = None
                if User.objects.filter(username=email_id).exists():
                    return Response({"success": False, "message": "Email ID already exist"}, status=HTTPStatus.OK)
                else:
                    check_rc = Vehicle.objects.filter(number_plate=number_plate).first()
                    if check_rc:
                        return Response(
                            {"success": False, "message": "Vehicle with this number plate already exists"}
                            , status=HTTPStatus.OK)
                    else:
                        profile = User.objects.create(first_name=f_name, last_name=l_name, age=age, address=address,
                                                      street=street, city=city, country=country, username=email_id)
                        profile.set_password(password)
                        profile.save()
                        profile_id = profile.pk

                        Vehicle.objects.create(number_plate=number_plate, brand=brand, model=model, user_id=profile_id)

                        # user = User.objects.create(username=email_id)
                        # user.set_password(password)
                        # user.save()

                        return Response(
                            {"success": True, "message": "User registered successfully"}
                            , status=HTTPStatus.OK)
            else:
                return Response({"success": False, "message": "Please enter vehicle details"}, status=HTTPStatus.OK)

        except Exception as e:
            traceback.print_exc()
            return Response({"success": False, "message": str(e)}, status=HTTPStatus.OK)

    def put(self, request):
        try:
            body_data = request.data
            f_name = body_data['f_name']
            l_name = body_data['l_name']
            age = body_data['age']
            address = body_data['address']
            street = body_data['street']
            city = body_data['city']
            country = body_data['country']
            user_id = body_data['user_id']

            profile = User.objects.filter(id=user_id).first()
            profile.first_name = f_name
            profile.last_name = l_name
            profile.age = age
            profile.address = address
            profile.street = street
            profile.city = city
            profile.country = country
            profile.save()

            return Response(
                {"success": True, "message": "Profile updated successfully"}, status=HTTPStatus.OK)
        except Exception as e:
            traceback.print_exc()
            return Response({"success": False, "message": str(e)}, status=HTTPStatus.OK)



class MyAdvertisement(GenericAPIView):

    def post(self, request):
        try:
            body_data = request.data
            title = body_data['title']
            description = body_data['description']
            price = body_data['price']
            vehicle_id = body_data['vehicle_id']
            user_id = body_data['user_id']

            check_adv = Advertisement.objects.filter(vehicle_id=vehicle_id).first()
            if check_adv:
                return Response(
                    {"success": False, "message": "Advertisement with this vehicle already exists"}
                    , status=HTTPStatus.OK)
            else:
                Advertisement.objects.create(vehicle_id=vehicle_id, user_id=user_id, title=title,
                                             description=description, price_per_km=price, datetime=datetime.now())
                return Response(
                    {"success": True, "message": "Advertisement posted successfully"}
                    , status=HTTPStatus.OK)

        except Exception as e:
            traceback.print_exc()
            return Response({"success": False, "message": str(e)}, status=HTTPStatus.OK)

    def get(self, request):
        try:
            body_data = request.data
            user_id = body_data['user_id']
            get_adv = Advertisement.objects.filter(user_id=user_id)
            if get_adv:
                serializer = GetAdvertisementSerializers(get_adv, many=True)
                return Response(
                    {"success": True, "message": "Showing all Advertisements", "data": serializer.data}
                    , status=HTTPStatus.OK)
            else:
                return Response(
                    {"success": True, "message": "No Advertisements posted", "data": []}
                    , status=HTTPStatus.OK)

        except Exception as e:
            traceback.print_exc()
            return Response({"success": False, "message": str(e)}, status=HTTPStatus.OK)

    def delete(self, request):
        try:
            body_data = request.data
            user_id = body_data['user_id']
            vehicle_id = body_data['vehicle_id']

            advObj = Advertisement.objects.get(user_id=user_id,vehicle_id=vehicle_id)
            advObj.delete()
            return Response({"success": True, "message": "Advertisement deleted successfully"}, status=HTTPStatus.OK)

        except Exception as e:
            traceback.print_exc()
            return Response({"success": False, "message": str(e)}, status=HTTPStatus.OK)

    def put(self, request):
        try:
            body_data = request.data
            title = body_data['title']
            description = body_data['description']
            price = body_data['price']
            vehicle_id = body_data['vehicle_id']
            user_id = body_data['user_id']

            advObj = Advertisement.objects.filter(user_id=user_id,vehicle_id=vehicle_id).first()
            if advObj:
                advObj.title = title
                advObj.description = description
                advObj.price_per_km = price
                advObj.save()

                return Response({"success": True, "message": "Advertisement updated successfully"},
                                status=HTTPStatus.OK)
            else:
                return Response({"success": False, "message": "No Advertisement posted"},
                                status=HTTPStatus.OK)

        except Exception as e:
            traceback.print_exc()
            return Response({"success": False, "message": str(e)}, status=HTTPStatus.OK)


class MyVehicle(GenericAPIView):
    def get(self, request):
        try:
            body_data = request.data
            user_id = body_data['user_id']

            vehicleobj = Vehicle.objects.filter(user_id=user_id)
            if vehicleobj:
                serializer = ViewVehicleSerializers(vehicleobj, many=True)
                return Response(
                    {"success": True, "message": "Showing all Vehicles", "data": serializer.data}
                    , status=HTTPStatus.OK)
            else:
                return Response(
                    {"success": True, "message": "No Vehicles added", "data": []}
                    , status=HTTPStatus.OK)

        except Exception as e:
            traceback.print_exc()
            return Response({"success": False, "message": str(e)}, status=HTTPStatus.OK)

    def post(self, request):
        try:
            body_data = request.data
            number_plate = body_data['number_plate']
            model = body_data['model']
            brand = body_data['brand']
            user_id = body_data['user_id']

            check_rc = Vehicle.objects.filter(number_plate=number_plate).first()
            if check_rc:
                return Response({"success": False, "message": "Vehicle with this number plate already exists"},
                                status=HTTPStatus.OK)
            else:
                Vehicle.objects.create(number_plate=number_plate, brand=brand, model=model, user_id=user_id)
                return Response({"success": True, "message": "Vehicle added successfully"},
                                status=HTTPStatus.OK)

        except Exception as e:
            traceback.print_exc()
            return Response({"success": False, "message": str(e)}, status=HTTPStatus.OK)

    def put(self, request):
        try:
            body_data = request.data
            number_plate = body_data['number_plate']
            model = body_data['model']
            brand = body_data['brand']
            user_id = body_data['user_id']
            vehicle_id = body_data['vehicle_id']

            vehobj = Vehicle.objects.filter(user_id=user_id, id=vehicle_id).first()
            if vehobj:
                vehobj.number_plate = number_plate
                vehobj.model = model
                vehobj.brand = brand
                vehobj.save()
                return Response({"success": True, "message": "Vehicle updated successfully"},
                                status=HTTPStatus.OK)
            else:
                return Response({"success": False, "message": "Vehicle not found"},
                                status=HTTPStatus.OK)

        except Exception as e:
            traceback.print_exc()
            return Response({"success": False, "message": str(e)}, status=HTTPStatus.OK)

    def delete(self, request):
        try:
            body_data = request.data
            user_id = body_data['user_id']
            vehicle_id = body_data['vehicle_id']

            vehicleObj = Vehicle.objects.get(user_id=user_id, id=vehicle_id)
            vehicleObj.delete()
            return Response({"success": True, "message": "Vehicle deleted successfully"}, status=HTTPStatus.OK)
        except Exception as e:
            traceback.print_exc()
            return Response({"success": False, "message": str(e)}, status=HTTPStatus.OK)


class ViewAdvertisement(GenericAPIView):
    def get(self, request):
        try:
            body_data = request.data
            user_id = body_data['user_id']

            getAdv = Advertisement.objects.all().exclude(user_id=user_id)
            if getAdv:
                serializer = ViewAdvertisementSerializers(getAdv, many=True)

                return Response(
                    {"success": True, "message": "Vehicle deleted successfully", "data": serializer.data}
                    , status=HTTPStatus.OK)
        except Exception as e:
            traceback.print_exc()
            return Response({"success": False, "message": str(e)}, status=HTTPStatus.OK)

