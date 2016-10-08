"""
    Created by: @pdonaire1
    Ing. Pablo Alejandro Gonzalez Donaire
"""
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from django.core import serializers

def clean_serlialized_object(model, length, i=0):
    model[i]['fields']['id'] = model[i]['pk']
    del model[i]['pk']
    del model[i]['model']
    model[i] = model[i]['fields']
    if i < length-1:
        clean_serlialized_object(model, length, i+1)
    return model

def build_json_object(model):
    model = serializers.serialize("json", model)
    model = JSONParser().parse(BytesIO(model))
    if len(model) > 0:
        return clean_serlialized_object(model, len(model))
    return [{}]
