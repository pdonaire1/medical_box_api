"""
    Created by: @pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
"""
from django.contrib.auth.models import User
from rooms.serializers import RoomSerializer
from django.http import JsonResponse
from rest_framework import (
	status, viewsets, filters, serializers)
from rest_framework.response import Response
from dry_rest_permissions.generics import DRYPermissions
from utils.functions import build_json_object
from clinics.models import Clinic
from rooms.models import Room
from rest_framework.decorators import detail_route, list_route
from django.utils.translation import ugettext as _

class RoomViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Patients.
    > Parameters:

      * Create: POST /api/rooms/ (login required as a Clinic in field created_by or in ClinicAdmin) => **clinic_id, room, (Optionals => floor)**.
      * Consult All: GET /api/rooms/.
      * Consult Rooms from Clinic: GET /api/rooms/clinic/ => {"clinic_id"}.
      * Consult One: GET /api/rooms/ID.
      * Update: PATCH or PUT /api/rooms/ID (login required as a Doctor) => room, **{(Optionals)-> {"floor"}**
      * Delete: DELETE /api/rooms/ID.
      * To Authenticate /api/api-token-auth/ parameters => **{"username", "password"}**
    """
    model = Room
    serializer_class = RoomSerializer
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    permission_classes = (DRYPermissions,)

    def get_queryset(self):
        return Room.objects.all()

    def perform_create(self, serializer):
        data = self.request.data
        if not "clinic_id" in data:
            raise serializers.ValidationError(
                {"error": _('Invalid fields'), "status": 400})

        clinic = Clinic.objects.get(id=data["clinic_id"])
        if clinic.is_admin(self.request.user):
            serializer.save(clinic_id=data['clinic_id'])
        else:
            raise serializers.ValidationError(
                {
                    "error": _('You have to be registred as an user admin of this clinic'),
                    "status": 400
                })


    @list_route(methods=['get'], url_path='clinic')
    def clinic(self, request):
        clinic = Clinic.objects.get(id=request.GET.get('clinic_id'))
        rooms = Room.objects.filter(clinic=clinic)
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)

