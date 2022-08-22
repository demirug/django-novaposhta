from django.urls import path

from novaposhta_api.api.views import AreaList, CityList, WareHouseTypeList, WareHouseList

urlpatterns = [
    path('area/', AreaList.as_view(), name="area"),
    path('city/', CityList.as_view(), name="city"),
    path('warehouse-type/', WareHouseTypeList.as_view(), name="warehouse-types"),
    path('warehouse/', WareHouseList.as_view(), name="warehouse"),
]