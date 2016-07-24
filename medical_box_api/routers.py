"""
    Created by: pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
"""
from rest_framework.routers import DefaultRouter, SimpleRouter
from patients.views import PatientViewSet
from doctors.views import DoctorViewSet
from clinics.views import ClinicViewSet
from specialities.views import SpecialityViewSet
from rooms.views import RoomViewSet

# router = SimpleRouter()
router = DefaultRouter()
# ------------------------------------------
router.register(r'patients', PatientViewSet, 'patients')
router.register(r'doctors', DoctorViewSet, 'doctors')
router.register(r'clinics', ClinicViewSet, 'clinics')
router.register(r'specialities', SpecialityViewSet, 'specialities')
router.register(r'rooms', RoomViewSet, 'rooms')

# urlpatterns = router.urls