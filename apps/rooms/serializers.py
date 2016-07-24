"""
    Created by: @pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from rooms.models import Room
from utils.serializers import UserSerializer

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fileds = ("id", "clinic", "room", "floor")
        depth = 1