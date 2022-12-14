import asyncio
import json

from novaposhta_api.models import *
from novaposhta_api.scraping import NP_Scrapping


class Updater:

    def __init__(self, scrapping: NP_Scrapping):
        self.scrapping = scrapping

    def rebuild_data(self):
        NP_WareHouse.objects.all().delete()
        NP_WareHouseType.objects.all().delete()
        NP_City.objects.all().delete()
        NP_Area.objects.all().delete()
        NP_CargoType.objects.all().delete()
        self.update_data()

    async def _update_data(self):
        await asyncio.gather(
            self.register_cargo_types(),
            self.register_warehouse_types(),
            self.register_areas(),
            self.register_cities(),
            self.register_warehouses(),
        )

    def update_data(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._update_data())
        loop.close()

    async def register_cargo_types(self):
        for elem in await self.scrapping.common.get_cargo_types():
            NP_CargoType(json=json.dumps(elem))

    async def register_warehouse_types(self):
        for elem in await self.scrapping.address.get_warehouse_types():
            NP_WareHouseType(json=json.dumps(elem))

    async def register_warehouses(self):
        for elem in await self.scrapping.address.get_warehouse_all():
            NP_WareHouse(json=json.dumps(elem))

    async def register_areas(self):
        for elem in await self.scrapping.address.get_areas():
            NP_Area(json=json.dumps(elem))

    async def register_cities(self):
        for elem in await self.scrapping.address.get_all_cities():
            NP_City(json=json.dumps(elem))
