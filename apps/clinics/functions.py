"""
    Created by: @pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
    created at: 08 Jan 2017
"""
from clinics.models import Clinic
from django.db.models import Q

def get_clinics_filtered_query(request):
        """
        Get clinics by:
        filtering params: 
        > order = options => "desc"
        > order_by = options => first_name, last_name, name, zip_code, address, phone_one, phone_two, country_name, city_name
        > doctor_first_name
        > doctor_last_name
        > name
        > zip_code
        > address
        > phone
        > country_name
        """
        clinics = Clinic.objects.filter(is_active=True)
        order_by = "id"
        order = ""
        if 'order_by' in request and request['order_by'] is not None:
            if 'order' in request and request['order'].lower() == "desc":
                order_by = "-"
            if request['order_by'] == "first_name":
                order_by = "created_by__first_name"
            elif request['order_by'] == "last_name":
                order_by = "created_by__last_name"
            elif request['order_by'] == "name":
                order_by = "name"
            elif request['order_by'] == "zip_code":
                order_by = "zip_code"
            elif request['order_by'] == "address":
                order_by = "address"
            elif request['order_by'] == "phone_one":
                order_by = "phone_one"
            elif request['order_by'] == "phone_two":
                order_by = "phone_two"
            elif request['order_by'] == "country_name":
                order_by = "country__name"
            elif request['order_by'] == "city_name":
                order_by = "city__name"

        if 'doctor_last_name' in request and request['doctor_first_name'] is not None:
            clinics = clinics.filter(
                Q(created_by__first_name__icontains=request['doctor_first_name']) |
                Q(doctors__name__icontains=request['doctor_first_name']) )
        if 'doctor_last_name' in request and request['doctor_last_name'] is not None:
            clinics = clinics.filter(
                Q(created_by__last_name__icontains=request['doctor_last_name']) |
                Q(doctors__name__icontains=request['doctor_last_name']) )
        if 'name' in request and request['name'] is not None:
            clinics = clinics.filter(name__icontains=request['name'])
        if 'zip_code' in request and request['zip_code'] is not None:
            clinics = clinics.filter(zip_code__icontains=request['zip_code'])
        if 'address' in request and request['address'] is not None:
            clinics = clinics.filter(address__icontains=request['address'])
        if 'phone' in request and request['phone'] is not None:
            clinics = clinics.filter(
                Q(phone_one__icontains=request['phone']) |
                Q(phone_two__icontains=request['phone']))
        if 'country_name' in request and request['country_name'] is not None:
            clinics = clinics.filter(country__name__icontains=request['country_name'])
        if 'city_name' in request and request['city_name'] is not None:
            clinics = clinics.filter(city__name__icontains=request['city_name'])

        return clinics.order_by("%s%s"%(order, order_by))