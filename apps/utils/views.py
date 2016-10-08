"""
    Created by: @pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
"""
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import filters, status, viewsets
from rest_framework.decorators import detail_route, list_route
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

class ChangePasswordViewSet(APIView):
    
    def get(self, request, format=None):
        return Response([{
            "message": "fields {old_password, new_password}"}])

    def post(self, request, format=None):
        """
            This function recibe: old_password, new_password
        """
        user = request.user
        old_password = request.data["old_password"]
        new_password = request.data["new_password"]
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(
                [{"message": "password cambiada", "success": True}], 
                status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)