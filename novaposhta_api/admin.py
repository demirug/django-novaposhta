from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .mixins import NP_AdminReadOnlyMixin
from .models import NP_Area, NP_City, NP_WareHouseType, NP_WareHouse, NP_CargoType, NP_Document


@admin.register(NP_Area)
class NP_AreaModelAdmin(NP_AdminReadOnlyMixin, ModelAdmin):
    list_display = ['Description', 'Ref']
    search_fields = ['Description']


@admin.register(NP_Document)
class NP_DocumentModelAdmin(NP_AdminReadOnlyMixin, ModelAdmin):
    list_display = ['IntDocNumber', 'Ref']
    search_fields = ['IntDocNumber']


@admin.register(NP_CargoType)
class NP_CargoTypeModelAdmin(NP_AdminReadOnlyMixin, ModelAdmin):
    list_display = ['Description', 'Ref']


@admin.register(NP_City)
class NP_CityModelAdmin(NP_AdminReadOnlyMixin, ModelAdmin):
    list_display = ['Description', 'Ref']
    search_fields = ['Description']
    list_filter = ['Area']


@admin.register(NP_WareHouseType)
class NP_WareHouseTypeModelAdmin(NP_AdminReadOnlyMixin, ModelAdmin):
    list_display = ['Description', 'Ref']


@admin.register(NP_WareHouse)
class NP_WareHouseModelAdmin(NP_AdminReadOnlyMixin, ModelAdmin):
    list_display = ['City', 'Type', 'Number', 'Ref']
    search_fields = ['City__Description']
    list_filter = ['Type', 'WarehouseStatus', 'City__Area']
    exclude = ('DenyToSelect',)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        fields.append('AllowedSelect')
        return fields

    def AllowedSelect(self, obj):
        return not obj.DenyToSelect
