from rest_framework.generics import ListAPIView

from novaposhta_api.api.serializers import AreaSerializer, WareHouseTypeSerializer, CitiesSerializer, \
    WareHousesSerializer
from novaposhta_api.models import NP_Area, NP_WareHouseType, NP_City, NP_WareHouse
from django_filters import rest_framework as filters


class AreaList(ListAPIView):
    queryset = NP_Area.objects.all()
    serializer_class = AreaSerializer


class WareHouseTypeList(ListAPIView):
    queryset = NP_WareHouseType.objects.all()
    serializer_class = WareHouseTypeSerializer


class CityList(ListAPIView):
    queryset = NP_City.objects.all()
    serializer_class = CitiesSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('Area',)


class WareHouseList(ListAPIView):
    queryset = NP_WareHouse.objects.all()
    serializer_class = WareHousesSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('City', 'Type', 'Number', 'WarehouseStatus')
