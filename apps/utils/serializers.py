from django.contrib.auth.models import User
from doctors.models import Doctor
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')

class ClinicSerializerGeneral(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('id',  'name', 'phone_number', 'is_active')

