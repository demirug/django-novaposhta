from django.contrib import admin

from .models import NP_Area, NP_City, NP_WareHouseType, NP_WareHouse

admin.site.register(NP_Area)
admin.site.register(NP_City)
admin.site.register(NP_WareHouseType)
admin.site.register(NP_WareHouse)