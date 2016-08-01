from django.contrib.auth.models import User
from specialities.serializers import SpecialitySerializer
from django.http import JsonResponse
from rest_framework import (
	status, viewsets, filters, serializers)
from rest_framework.response import Response
from dry_rest_permissions.generics import DRYPermissions
from specialities.models import Speciality

class SpecialityViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Patients.
    > Parameters:

      * Create: POST /api/patients/ => **phone_number, (Optionals => first_name, last_name, address), email, password**.
      * Consult All: GET /api/patients/ => (Optionals: **phone_number, address, is_active, user__first_name, user__last_name, user__email**).
      * Consult One: GET /api/patients/ID.
      * Update: PATCH or PUT => **{"id", (Optionals)-> {"phone_number", "address", "user": {"first_name", "last_name", "id"}}**
      * Delete: DELETE /api/patients/ID.
      * To Authenticate /api/api-token-auth/ parameters => **{"username", "password"}**
    """
    model = Speciality
    serializer_class = SpecialitySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    # permission_classes = (DRYPermissions,)

    def get_queryset(self):
        return Speciality.objects.all()

