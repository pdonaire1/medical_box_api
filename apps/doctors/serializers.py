"""
    Created by: @pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from doctors.models import Doctor
from utils.serializers import UserSerializer

class DoctorSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ('id', 'name', 'phone_number', 'is_active',
            'user'
            )
        depth = 1

    def get_user(self, doctor):
        if hasattr(doctor, 'user'):
            request = self.context['request']
            return UserSerializer(doctor.user, context={'request': request}).data
        else:
            return None

    def get_is_active(self, doctor):
        if hasattr(doctor, 'is_active'):
            return doctor.is_active
        else: 
            return None
