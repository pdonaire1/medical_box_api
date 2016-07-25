"""
WSGI config for medical_box_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

""" Original ->
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medical_box_api.settings")

application = get_wsgi_application()
"""
"""
from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())
"""

# source: https://djangogirls.gitbooks.io/django-girls-tutorial-extensions/content/heroku/
from django.core.wsgi import get_wsgi_application
from dj_static import Cling
application = Cling(get_wsgi_application())
from whitenoise.django import DjangoWhiteNoise
application = DjangoWhiteNoise(application)
