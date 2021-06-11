from main.models import Airport
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class AirportSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Airport
        fields = ['name', 'id']
        geo_field = 'point'