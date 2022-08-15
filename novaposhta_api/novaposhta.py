from django.conf import settings

from .models import NP_Area, NP_City, NP_WareHouseType, NP_WareHouse
from .scraping import NP_Scrapping
from .singleton import Singleton


class Novaposhta(Singleton):

    def __init__(self):
        self.api_key = settings.NOVAPOSHTA_KEY
        self.scrapping = NP_Scrapping(self.api_key)

    def rebuild_data(self):
        NP_WareHouse.objects.all().delete()
        NP_WareHouseType.objects.all().delete()
        NP_City.objects.all().delete()
        NP_Area.objects.all().delete()
        self.update_data()

    def update_data(self):
        self.register_warehouse_types()
        self.register_areas()
        self.register_cities()
        self.register_warehouses()

    def register_warehouse_types(self):
        NP_WareHouseType.objects.bulk_create([NP_WareHouseType(
            description=elem['Description'],
            description_ru=elem['DescriptionRu'],
            ref=elem["Ref"])
            for elem in self.scrapping.address.get_warehouse_types()], ignore_conflicts=True)

    def register_warehouses(self):
        cities = NP_City.objects.all()
        warehouses_types = NP_WareHouseType.objects.all()

        NP_WareHouse.objects.bulk_create([NP_WareHouse(
            ref=elem['Ref'],
            city=cities.get(ref=elem['CityRef']),
            type=warehouses_types.get(ref=elem['TypeOfWarehouse']),
            status=elem['WarehouseStatus'],
            siteKey=int(elem['SiteKey']),
            description=elem['Description'],
            description_ru=elem['DescriptionRu'],
            denyToSelect=bool(elem['DenyToSelect']),
            number=int(elem['Number']),
            maxDeclaredCost=int(elem['MaxDeclaredCost']),
            totalMaxWeightAllowed=int(elem['TotalMaxWeightAllowed']),
            placeMaxWeightAllowed=int(elem['PlaceMaxWeightAllowed']),
            dimensions_max_width=int(elem['SendingLimitationsOnDimensions']['Width']),
            dimensions_max_height=int(elem['SendingLimitationsOnDimensions']['Height']),
            dimensions_max_length=int(elem['SendingLimitationsOnDimensions']['Length'])
        ) for elem in self.scrapping.address.get_warehouse_all()], ignore_conflicts=True)

    def register_areas(self):
        NP_Area.objects.bulk_create([NP_Area(
            description=elem['Description'],
            description_ru=elem['DescriptionRu'],
            areas_center=elem['AreasCenter'],
            ref=elem["Ref"])
            for elem in self.scrapping.address.get_areas()], ignore_conflicts=True)

    def register_cities(self):
        areas = NP_Area.objects.all()
        NP_City.objects.bulk_create([NP_City(
            description=elem['Description'],
            description_ru=elem['DescriptionRu'],
            ref=elem['Ref'],
            area=areas.get(ref=elem['Area']))
            for elem in self.scrapping.address.get_all_cities()], ignore_conflicts=True)
