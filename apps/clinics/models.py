"""
    Created by: @pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from cities_customized.models import Country, Region, City
from doctors.models import Doctor
from patients.models import Patient
from django.contrib.auth.models import User

@python_2_unicode_compatible
class Clinic(models.Model):
    created_by = models.ForeignKey(User)
    name = models.CharField(max_length=128)
    country = models.ForeignKey(Country)
    # region = models.ForeignKey(Region) ######
    city = models.ForeignKey(City)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=128)
    latitude = models.CharField(max_length=128, blank=True, null=True)
    longitude = models.CharField(max_length=128, blank=True, null=True)
    phone_one = models.CharField(max_length=50, blank=True, null=True)
    phone_two = models.CharField(max_length=50, blank=True, null=True)
    doctors = models.ManyToManyField(Doctor)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return '{0}'.format(self.id)

    def is_admin(self, user):
        if self.created_by == user:
            return True
        if ClinicAdmin.objects.filter(clinic=self, user=user).exists():
            return True
        return False
        
    ######################
    # Global Permissions #
    ######################

    @staticmethod
    def has_read_permission(request):
        return True

    @staticmethod
    def has_create_permission(request):
        if ( not request.user.is_anonymous()
            and Doctor.objects.filter(user = request.user).exists()):
            return True
        return False

    @staticmethod
    def has_write_permission(request):
        return True

    ######################
    # Object Permissions #
    ######################

    def has_object_write_permission(self, request):
        return True

    def has_object_clinic_doctors_permission(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated():
            is_admin = ClinicAdmin.objects.filter(
                clinic=self, user=request.user).exists()
            if self.created_by == request.user or is_admin:
                return True
        return False

    def has_object_clinic_admin_permission(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated():
            is_admin = ClinicAdmin.objects.filter(
                clinic=self, user=request.user).exists()
            if self.created_by == request.user or is_admin:
                return True
        return False

    def has_object_create_permission(self, request):
        if (not request.user.is_anonymous
            and Doctor.objects.filter(user = request.user).exists()):
            return True
        return False

    def has_object_read_permission(self, request):
        return True

    def has_object_update_permission(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated():
            is_admin = ClinicAdmin.objects.filter(
                clinic=self, user=request.user).exists()
            if self.created_by == request.user or is_admin:
                return True
        return False

    def has_object_destroy_permission(self, request):
        return False


@python_2_unicode_compatible
class ClinicAdmin(models.Model):
    user = models.ForeignKey(User)
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
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    ######################
    # Object Permissions #
    ######################

    def has_object_write_permission(self, request):
        return True

    def has_object_create_permission(self, request):
        return True

    def has_object_read_permission(self, request):
        return True

    def has_object_update_permission(self, request):
        return True

    def has_object_destroy_permission(self, request):
        return False

