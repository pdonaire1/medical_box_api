from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from cities_light.abstract_models import (AbstractCity, AbstractRegion,
    AbstractCountry)
from cities_light.receivers import connect_default_signals

@python_2_unicode_compatible
class Country(AbstractCountry):

    def __str__(self):
        return '{0}'.format(self.id)

connect_default_signals(Country)

@python_2_unicode_compatible
class Region(AbstractRegion):
    
    def __str__(self):
        return '{0}'.format(self.id)

connect_default_signals(Region)

@python_2_unicode_compatible
class City(AbstractCity):
    timezone = models.CharField(max_length=40)
    def __str__(self):
        return '{0}'.format(self.id)
        
connect_default_signals(City)


import cities_light
from cities_light.settings import ICity

def set_city_fields(sender, instance, items, **kwargs):
    instance.timezone = items[ICity.timezone]

cities_light.signals.city_items_post_import.connect(set_city_fields)
