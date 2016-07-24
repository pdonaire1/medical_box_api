"""
    Created by: @pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
"""
from django.contrib.auth.models import User
from doctors.serializers import DoctorSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from doctors.models import Doctor
from rest_framework import filters
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import serializers

class DoctorViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Patients.
    > Parameters:

      * Create: POST /api/doctors/ => **phone_number, name, email, password, (Optionas => first_name, last_name)**.
      * Consult All: GET /api/doctors/ => (Optionals: **phone_number, name, is_active, user__first_name, user__last_name, user__email**).
      * Consult One: GET /api/doctors/ID.
      * Update: PATCH or PUT /api/doctors/ID => **{"id", (Optionals)-> {"phone_number", "name", "user": {"first_name", "last_name", "id"}}**
      * Delete: DELETE /api/doctors/ID.
      * To Authenticate /api/api-token-auth/ parameters => **{"username", "password"}**
      * Countries: /api/countries/, Cities: /api/cities/
    """
    model = Doctor
    serializer_class = DoctorSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name', 'phone_number', 'is_active', 'user__first_name', 'user__last_name', 'user__email')
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    permission_classes = (DRYPermissions,)
    # Another option to filter: 
    # https://github.com/philipn/django-rest-framework-filters

    def get_queryset(self):
        return Doctor.objects.all()

    def perform_create(self, serializer):
        data = self.request.data
        first_name = data["first_name"] if "first_name" in data else None
        last_name = data["last_name"] if "last_name" in data else None
        email = data["email"]
        password = data["password"]
        if email:
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if Doctor.objects.filter(user=user).exists():
                    raise serializers.ValidationError(
                        {"error":'Doctor already exists', "status": 400, "exists": True})

                if not user.check_password(password):
                    raise serializers.ValidationError(
                        {"error":'Password do not belong', "status": 400})
                else:
                    if email:
                        user.username=email
                        user.email=email
                    if first_name:
                        user.first_name=first_name
                    if last_name:
                        user.last_name=last_name
                    user.save()
            else:
                user = User.objects.create_user(
                    username=email,
                    first_name=first_name,
                    last_name=last_name,
                    email=email)
                user.set_password(password)
                user.save()
            serializer.save(user=user, is_active=True)
        else:
            raise serializers.ValidationError(
                {"error":'Invalid fields', "status": 400})

    def perform_update(self, serializer):
        id = self.request.data["user"]["id"]
        user = User.objects.get(id=id)
        user.first_name = self.request.data["user"]["first_name"]
        user.last_name = self.request.data["user"]["last_name"]
        user.save()
        serializer.save()
