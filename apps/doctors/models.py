"""
    Created by: @pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
"""
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from specialities.models import Speciality

@python_2_unicode_compatible
class Doctor(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=128, blank=True, null=True) # like a leyend
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return '{0}'.format(self.id)

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
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    ######################
    # Object Permissions #
    ######################

    def has_object_create_permission(self, request):
        return True

    def has_object_read_permission(self, request):
        return True

    def has_object_update_permission(self, request):
        return request.user == self.user
        # return True

    def has_object_destroy_permission(self, request):
        return False


class DoctorSpeciality(models.Model):
    speciality = models.ForeignKey(Speciality)
    doctor = models.ForeignKey(Doctor)
    consult_price = models.FloatField()
