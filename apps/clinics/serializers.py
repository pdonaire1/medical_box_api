"""
    Created by: @pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from clinics.models import Clinic
from utils.serializers import UserSerializer
from doctors.serializers import DoctorSerializer

class ClinicSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Clinic
        exclude = ('is_active', )
        depth = 1

    def get_created_by(self, clinic):
        if hasattr(clinic, 'created_by'):
            request = self.context['request']
            return UserSerializer(clinic.created_by, context={'request': request}).data
        else:
            return None

    def get_doctors(self, room):
        if hasattr(clinic, 'doctors'):
            request = self.context['request']
            return DoctorSerializer(room.doctors, context={'request': request}).data