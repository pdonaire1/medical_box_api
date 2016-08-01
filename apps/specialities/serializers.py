from rest_framework import serializers
from django.contrib.auth.models import User
from specialities.models import Speciality
from utils.serializers import UserSerializer

class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        depth = 1