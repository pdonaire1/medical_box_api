"""
    Created by: @pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
"""
from rest_framework import serializers
from django.contrib.auth.models import User
# from validate_email import validate_email
from patients.models import Patient
from utils.serializers import UserSerializer

class PatientSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ('id', 'phone_number', 'address', 'is_active',
            'user')
        depth = 1

    def get_user(self, doctor):
        request = self.context['request']
        if hasattr(doctor, 'user'):
            return UserSerializer(doctor.user, context={'request': request}).data
        else:
            return None

    def get_is_active(self, doctor):
        if hasattr(doctor, 'is_active'):
            return doctor.is_active
        else: 
            return None
