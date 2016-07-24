"""
    Created by: @pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from clinics.models import Clinic
from doctors.models import Doctor
from clinics.models import ClinicAdmin

@python_2_unicode_compatible
class Room(models.Model):
    floor = models.CharField(max_length=35, blank=True, null=True)
    room = models.CharField(max_length=35)
    clinic = models.ForeignKey(Clinic)

    def __str__(self):
        return '{0}'.format(self.id)

    ######################
    # Global Permissions #
    ######################

    @staticmethod
    def has_read_permission(request):
        return True

    @staticmethod
    def has_create_permission(request):
        if (not request.user.is_anonymous() and 
            ClinicAdmin.objects.filter(user=request.user).exists()):
            return True
        return False

    @staticmethod
    def has_write_permission(request):
        return True

    ######################
    # Object Permissions #
    ######################

    def has_object_create_permission(self, request):
        if (not request.user.is_anonymous() and 
            ClinicAdmin.objects.filter(user=request.user).exists()):
            return True
        return False        
    def has_object_read_permission(self, request):
        return True

    def has_object_update_permission(self, request):
        if (not request.user.is_anonymous() and 
            ClinicAdmin.objects.filter(user=request.user).exists()):
            return True
        return False  

    def has_object_destroy_permission(self, request):
        if (not request.user.is_anonymous() and 
            ClinicAdmin.objects.filter(user=request.user).exists()):
            return True
        return False  



@python_2_unicode_compatible
class Schedule(models.Model):
    init = models.TimeField()
    end = models.TimeField()
    week_day = models.IntegerField()

    def __str__(self):
        return '{0}'.format(self.id)

@python_2_unicode_compatible
class RoomDoctor(models.Model):
    room = models.ForeignKey(Room)
    doctor = models.ForeignKey(Doctor)
    schedule = models.ForeignKey(Schedule)
    

    def __str__(self):
        return '{0}'.format(self.id)

