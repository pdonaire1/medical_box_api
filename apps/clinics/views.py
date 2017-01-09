"""
    Created by: @pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
"""
from django.contrib.auth.models import User
from clinics.serializers import ClinicSerializer
from clinics.functions import get_clinics_filtered_query
from django.http import JsonResponse
from rest_framework import (
	status, viewsets, filters, serializers)
from rest_framework.response import Response
from dry_rest_permissions.generics import DRYPermissions
from utils.functions import build_json_object
from clinics.models import Clinic, ClinicAdmin
from cities_customized.models import Country, Region, City
from doctors.models import Doctor
from rest_framework.decorators import detail_route, list_route
from django.utils.translation import ugettext as _

class ClinicViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Clinics.
    > Parameters:

      * Create: POST /api/clinics/ (login required as a Doctor) => **name, country_id, city_id, address, (Optionals => zip_code, latitude, longitude, phone_one, phone_two) In headers {"Autorization": "Token XXX"} of the doctor**.
      * Find Clinics: GET /api/clinics/find_clinic Params (optionals)=> limit, offset, order = options => "desc", order_by = options => first_name, last_name, name, zip_code, address, phone_one, phone_two, country_name, city_name, doctor_first_name, doctor_last_name, name, zip_code, address, phone, country_name
      * Consult All: GET /api/clinics/ => (Optionals: **phone_number, address, is_active, user__first_name, user__last_name, user__email**).
      * Consult One: GET /api/clinics/ID.
      * Update: PATCH or PUT /api/clinics/ID (login required as a Doctor) => **{(Optionals)-> {"name", "zip_code", "address", "latitude", "longitude", "phone_one", "phone_two", "country_id", "city_id" }**
      * Update Doctors: GET, POST /api/clinics/ID/clinic_doctors/ (login required as a Doctor who has created the clinic) => **{"doctors": [1,2,3]}  ->this will remove all the doctors registered and will to add the doctors from the list**  (USERS' IDS ARE NOT THE SAME THAT DOCTOR'S IDS).
      * Update Admin: GET, POST /api/clinics/ID/clinic_admin/ => **{"users": [1,2,3]}** (USERS' IDS ARE NOT THE SAME THAT DOCTOR'S IDS).
      * Delete: POST /api/clinics/ID/delete_recover => **if is active, will and is posted, this object will be disable or removed and vice versa**.
      * To Authenticate /api/api-token-auth/ parameters => **{"username", "password"}**
    """
    model = Clinic
    serializer_class = ClinicSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    permission_classes = (DRYPermissions,)

    def get_queryset(self):
        return Clinic.objects.filter(is_active=True)

    def perform_create(self, serializer):
        data = self.request.data
        clinic_obj = Clinic()
        if clinic_obj.is_already_created(data, self.request.user):
            raise serializers.ValidationError(
                {"error": _('Clinic already exists'), "status": 400})
        if ( "country_id" in data and 
            "city_id" in data):
            serializer.save(
                country_id=data["country_id"],
                city_id=data["city_id"],
                created_by_id=self.request.user.id,
                is_active=True)
        else:
            raise serializers.ValidationError(
                {"error": _('Invalid fields'), "status": 400})


    @detail_route(methods=['get', 'post'], url_path='clinic_doctors')
    def clinic_doctors(self, request, pk=None):
        clinic = Clinic.objects.get(id=pk)
        if request.method == "POST":
            if not clinic.has_object_clinic_doctors_permission(request):
                raise serializers.ValidationError({
                    "error": _('You have to be registred as an user admin of this clinic'),
                    "status": 400
                    })
            doctors = Doctor.objects.filter(
                id__in=request.data['doctors'])
            clinic.doctors.clear() # Remove the old doctors)
            clinic.doctors.add(*doctors)# Add the doctors from the ids list
            doctors = build_json_object(clinic.doctors.all())
        return Response(build_json_object(clinic.doctors.all()))

    @detail_route(methods=['get', 'post'], url_path='clinic_admin')
    def clinic_admin(self, request, pk=None):
        clinic = Clinic.objects.get(id=pk)
        clinic_admin = ClinicAdmin.objects.filter(clinic__id=pk)
        if request.method == "POST":
            if not clinic.has_object_clinic_admin_permission(request):
                raise serializers.ValidationError({
                    "error": _('You have to be registred as an user admin of this clinic'),
                    "status": 400
                    })
            users = User.objects.filter(
                id__in=request.data['users'])
            clinic_admin.delete() # Remove old ClinicAdmin
            for i in users: # Add the users from the ids list
                admin = ClinicAdmin(user=i, clinic=clinic)
                admin.save()
            doctors = build_json_object(ClinicAdmin.objects.all())

        return Response(build_json_object(clinic_admin))

    @detail_route(methods=['get', 'post'], url_path='delete_recover')
    def delete_recover(self, request, pk=None):
        clinic = Clinic.objects.get(id=pk)
        clinic_admin = ClinicAdmin.objects.filter(clinic__id=pk)
        if request.method == "POST":
            if not clinic.has_object_clinic_admin_permission(request):
                raise serializers.ValidationError({
                    "error": _('You have to be registred as an user admin of this clinic'),
                    "status": 400
                    })
            if clinic.is_active:
                clinic.is_active = False
            else:
                clinic.is_active = True
            clinic.save()
            clinic_json = build_json_object([clinic])  
            del clinic_json[0]['doctors']
            return Response([{
                "success": True, "is_active": clinic.is_active,
                "clinic": clinic_json
            }])
        return Response([{"method": "POST, if is active, will and is posted, this object will be disable or removed and vice versa"}])

    @list_route(methods=['get'])
    def find_clinic(self, request):
        clinics = get_clinics_filtered_query(request.query_params)
        page = self.paginate_queryset(clinics)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(clinics, many=True)
        return Response(serializer.data)