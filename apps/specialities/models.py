from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Speciality(models.Model):
    name = models.CharField(max_length=250)


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
    	return True if request.user else False

    @staticmethod
    def has_write_permission(request):
        return True if request.user else False

    ######################
    # Object Permissions #
    ######################

    def has_object_create_permission(self, request):
        return True if request.user else False

    def has_object_read_permission(self, request):
        return True

    def has_object_update_permission(self, request):
    	return False

    def has_object_destroy_permission(self, request):
        return False