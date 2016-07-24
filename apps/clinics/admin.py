"""
    Created by: @pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
"""
from django.contrib import admin
from appointments.models import Appointment
from cities_customized.models import Country, Region, City
from clinics.models import Clinic, ClinicAdmin
from doctors.models import Doctor, DoctorSpeciality
from patients.models import Patient
from rooms.models import Room, Schedule, RoomDoctor
from specialities.models import Speciality

admin.site.register(Appointment)
admin.site.register(Clinic)
admin.site.register(ClinicAdmin)
admin.site.register(Doctor)
admin.site.register(DoctorSpeciality)
admin.site.register(Patient)
admin.site.register(Room)
admin.site.register(Schedule)
admin.site.register(Speciality)
