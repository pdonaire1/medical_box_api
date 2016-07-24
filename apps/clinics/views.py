"""
    Created by: @pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
"""
from django.contrib.auth.models import User
from clinics.serializers import ClinicSerializer
from django.http import JsonResponse
from rest_framework import (
	status, viewsets, filters, serializers)
from rest_framework.response import Response
from dry_rest_permissions.generics import DRYPermissions
from utils.functions import build_json_object
from clinics.models import Clinic, ClinicAdmin
from cities_customized.models import Country, Region, City
from doctors.models import Doctor
from rest_framework.decorators import detail_route

class ClinicViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Clinics.
    > Parameters:

      * Create: POST /api/clinics/ (login required as a Doctor) => **name, country_id, city_id, address, (Optionals => zip_code, latitude, longitude, phone_one, phone_two)**.
      * Consult All: GET /api/clinics/ => (Optionals: **phone_number, address, is_active, user__first_name, user__last_name, user__email**).
      * Consult One: GET /api/clinics/ID.
      * Update: PATCH or PUT /api/clinics/ID (login required as a Doctor) => **{(Optionals)-> {"name", "zip_code", "address", "latitude", "longitude", "phone_one", "phone_two", "country_id", "city_id" }**
      * Update Doctors: GET, POST /api/clinics/ID/clinic_doctors/ (login required as a Doctor who has created the clinic) => **{"doctors": [1,2,3]}  ->this will remove all the doctors registered and will to add the doctors from the list**  (USERS' IDS ARE NOT THE SAME THAT DOCTOR'S IDS).
      * Update Admin: GET, POST /api/clinics/ID/clinic_admin/ => **{"users": [1,2,3]}** (USERS' IDS ARE NOT THE SAME THAT DOCTOR'S IDS).
      * Delete: DELETE /api/clinics/ID.
      * To Authenticate /api/api-token-auth/ parameters => **{"username", "password"}**
    """
    model = Clinic
    serializer_class = ClinicSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    permission_classes = (DRYPermissions,)

    def get_queryset(self):
        return Clinic.objects.all()

    def perform_create(self, serializer):
        if ( "country_id" in self.request.data and 
            "city_id" in self.request.data):
            serializer.save(
                country_id=self.request.data["country_id"],
                city_id=self.request.data["city_id"],
                created_by_id=self.request.user.id,
                is_active=True)
        else:
            raise serializers.ValidationError(
                {"error":'Invalid fields', "status": 400})


    @detail_route(methods=['get', 'post'], url_path='clinic_doctors')
    def clinic_doctors(self, request, pk=None):
        clinic = Clinic.objects.get(id=pk)
        if request.method == "POST":
            if not clinic.has_object_clinic_doctors_permission(request):
                raise serializers.ValidationError({
                    "error":'You have to be registred as a user admin of this clinic', 
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
                    "error":'You have to be registred as a user admin of this clinic', 
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
