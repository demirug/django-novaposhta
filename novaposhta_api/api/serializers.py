from rest_framework import serializers

from novaposhta_api.models import NP_Area, NP_City, NP_WareHouse, NP_WareHouseType


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NP_Area
        exclude = ['json']


class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NP_City
        exclude = ['json']


class WareHouseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NP_WareHouseType
        exclude = ['json']


class WareHousesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NP_WareHouse
        exclude = ['json']
