"""
    Created by: @pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
"""
# source: https://djangogirls.gitbooks.io/django-girls-tutorial-extensions/content/heroku/
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medical_box_api.settings")
from dj_static import Cling
application = Cling(get_wsgi_application())
from whitenoise.django import DjangoWhiteNoise
application = DjangoWhiteNoise(application)
