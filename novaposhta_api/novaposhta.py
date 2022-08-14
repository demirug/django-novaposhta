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
            ref=elem["Ref"])
            for elem in self.scrapping.address.get_warehouse_types()], ignore_conflicts=True)

    def register_warehouses(self):

        cities = NP_City.objects.all()
        warehouses_types = NP_WareHouseType.objects.all()

        NP_WareHouse.objects.bulk_create([NP_WareHouse(
            city=cities.get(ref=elem['CityRef']),
            type=warehouses_types.get(ref=elem['TypeOfWarehouse']),
            description=elem['Description'],
            number=elem['Number'],
            ref=elem['Ref'])
            for elem in self.scrapping.address.get_warehouse_all()], ignore_conflicts=True)

    def register_areas(self):
        NP_Area.objects.bulk_create([NP_Area(
            description=elem['Description'],
            areas_center=elem['AreasCenter'],
            ref=elem["Ref"])
            for elem in self.scrapping.address.get_areas()], ignore_conflicts=True)

    def register_cities(self):
        areas = NP_Area.objects.all()
        NP_City.objects.bulk_create([NP_City(
            description=elem['Description'],
            ref=elem['Ref'],
            area=areas.get(ref=elem['Area']))
            for elem in self.scrapping.address.get_all_cities()], ignore_conflicts=True)
